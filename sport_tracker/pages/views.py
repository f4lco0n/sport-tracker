from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.shortcuts import render, redirect
from django.http.response import HttpResponse
import xlwt

from game.models import SportGame, Match, Confirmation, ConfirmationMessage
from .forms import MatchForm, ConfirmationMessageForm, StatisticExportForm, RenewMatchForm
from . import utils


def home_view(request):
    return render(request, 'home.html')


@login_required
@csrf_exempt
def show_confirmations(request):
    if request.method == "POST":
        excluded_keys_list = ['csrfmiddlewaretoken', '_com']

        for (confirmation_id, choice) in request.POST.items():
            if any(exclude in confirmation_id for exclude in excluded_keys_list):
                continue
            confirmation = Confirmation.objects.get(id=confirmation_id)
            comment = request.POST[f"{confirmation_id}_com"]
            if choice == "confirmed":
                utils.set_confirmation_status(confirmation, Confirmation.STATUS_CONFIRMED, comment)
            if choice == "rejected":
                utils.set_confirmation_status(confirmation, Confirmation.STATUS_REJECTED, comment,
                                              rejected_by=request.user)

    matches_to_confirm = Confirmation.objects.filter(
        match__opponent=request.user,
        status=Confirmation.STATUS_PENDING_CONFIRMATION)  # here we get matches where current user was an opponent
    return render(request, "confirmations.html", {"confirmations": matches_to_confirm})


@login_required
def show_matches(request):
    confirmations = Confirmation.objects.filter(
        (Q(match__author=request.user) | Q(match__opponent=request.user)) & ~Q(status=Confirmation.STATUS_REJECTED))
    return render(request, 'matches.html', {"confirmations": confirmations})


@login_required
def show_rejected_matches(request):
    if request.method == "POST":
        excluded_keys_list = ['csrfmiddlewaretoken', '_com']
        for (rejection_id, name) in request.POST.items():
            if any(exclude in rejection_id for exclude in excluded_keys_list):
                continue
            rejection = Confirmation.objects.get(id=rejection_id)
            utils.set_confirmation_status(rejection, Confirmation.STATUS_PENDING_CONFIRMATION, rejection.comment)
    rejected_matches = Confirmation.objects.filter(
        (Q(match__author=request.user) | Q(match__opponent=request.user)) & Q(status=Confirmation.STATUS_REJECTED))
    return render(request, "rejected_matches.html", {"rejected": rejected_matches})


@login_required
def create_match(request):
    form = MatchForm(request.user)
    if request.method == "POST":
        form = MatchForm(request.user, data=request.POST)
        if form.is_valid():  # todo clean this
            form_game = form.cleaned_data["game"]
            result = form.cleaned_data["result"]
            opponent = form.cleaned_data["opponent"]
            game = SportGame.objects.get(name=form_game)
            opponent_object = User.objects.get(username=opponent)
            winner = form.cleaned_data["winner"]
            winner_object = User.objects.get(username=winner)
            match = Match(author=request.user,
                          game=game, result=result,
                          opponent=opponent_object,
                          winner=winner_object
                          )
            match.save()
            confirmation = Confirmation(match=match, status=Confirmation.STATUS_PENDING_CONFIRMATION)
            confirmation.save()

            return redirect("matches")

    return render(request, "new_match.html", {"form": form})


@login_required
def show_stats(request):
    user = request.user
    return render(request, "stats.html", {"all_matches": utils.get_user_played_matches_number(user),
                                          "won_matches": utils.get_user_won_matches_number(user),
                                          "lost_matches": utils.get_user_lost_matches_number(user),
                                          "pending_confirmations": utils.get_user_pending_confirmation_matches_number(
                                              user),
                                          "game_details": utils.get_user_details_in_each_game(user)})


@login_required
def message_about_match(request, pk, rej):
    form = ConfirmationMessageForm
    user = User.objects.get(id=pk)
    rejection = Confirmation.objects.get(id=rej)
    match_messages = ConfirmationMessage.objects.filter(confirmation=rejection).order_by("-id")
    if request.method == "POST":
        form = ConfirmationMessageForm(data=request.POST)
        if form.is_valid():
            message = form.cleaned_data["message"]
            confirmation_message = ConfirmationMessage(confirmation=rejection, message=message, author=request.user)
            confirmation_message.save()
            return redirect("message_about_match", pk, rej)
    return render(request, "message_about_match.html", {"to_user": user,
                                                        "rejection": rejection,
                                                        "form": form,
                                                        "messages": match_messages})


@login_required
def renew_match(request, pk, rej):
    user = User.objects.get(id=pk)
    rejection = Confirmation.objects.get(id=rej)
    match = Match.objects.get(id=rejection.match.id)
    form = RenewMatchForm(initial={"result": match.result, "winner": match.winner})
    if request.method == "POST":
        form = RenewMatchForm(data=request.POST)
        if form.is_valid():
            match.result = form.cleaned_data["result"]
            match.winner = User.objects.get(username=form.cleaned_data["winner"])
            rejection.status = Confirmation.STATUS_PENDING_CONFIRMATION
            #  todo remove confirmation messages
            match.save()
            rejection.save()
            return redirect("rejected_matches")
    return render(request, "renew_match.html", {
        "user": user, "rejection": rejection, "form": form
    })


@login_required
def export_view(request):
    form = StatisticExportForm
    if request.method == "POST":
        form = StatisticExportForm(data=request.POST)
        if form.is_bound and form.is_valid():
            return export_stats(form, request.user)
    return render(request, "export_stats.html", {"form": form})


def export_stats(form, user):
    timestamp = utils.get_timestamp()
    response = HttpResponse(content='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="stats-{timestamp}.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Stats")
    date_from = form.data.get('date_from', "")
    date_to = form.data.get('date_to', "")
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    columns = [
        "Rozegrane mecze", "Mecze wygrane", "Mecze przegrane"
    ]

    for col_num in range(len(columns)):
        ws.write(0, col_num, columns[col_num], font_style)

    ws.write(1, 0, utils.get_user_played_matches_number(user), font_style)
    ws.write(1, 1, utils.get_user_won_matches_number(user), font_style)
    ws.write(1, 2, utils.get_user_lost_matches_number(user), font_style)

    wb.save(response)
    return response
