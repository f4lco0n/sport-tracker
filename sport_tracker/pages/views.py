from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db.models import Q
from django.http import HttpResponseRedirect

from game.models import SportGame, Match, Confirmation, ConfirmationMessage
from django.shortcuts import render, redirect, get_object_or_404
from .forms import MatchForm, ConfirmationMessageForm

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
        if form.is_valid():
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
    game_details = utils.get_user_details_in_each_game(user)
    all_matches = utils.get_user_played_matches_number(user)
    won_matches = utils.get_user_won_matches_number(user)
    lost_matches = utils.get_user_lost_matches_number(user)
    pending_confirmations = utils.get_user_pending_confirmation_matches_number(user)
    return render(request, "stats.html", {"all_matches": all_matches,
                                          "won_matches": won_matches,
                                          "lost_matches": lost_matches,
                                          "pending_confirmations": pending_confirmations,
                                          "game_details": game_details})


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
