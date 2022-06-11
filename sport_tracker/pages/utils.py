from django.contrib.auth.models import User
from django.db.models import Q
from game.models import Confirmation, Match
from datetime import datetime


def get_timestamp() -> str:
    timestamp: datetime = datetime.now()
    return timestamp.strftime('%Y-%m/%d-%H%M%S')


def get_user_confirmations_number(user: User) -> int:
    return Confirmation.objects.filter(match__opponent=user, status=Confirmation.STATUS_PENDING_CONFIRMATION).count()


def get_user_rejected_matches_number(user: User) -> int:
    return Confirmation.objects.filter((Q(match__author=user) | Q(match__opponent=user)),
                                       status=Confirmation.STATUS_REJECTED).count()


def set_confirmation_status(confirmation: Confirmation, status: str, comment: str = "", rejected_by: User = None):
    confirmation.status = status
    confirmation.comment = comment
    confirmation.rejected_by = rejected_by
    confirmation.save()


def get_user_played_matches_number(user: User) -> int:
    return Match.objects.filter(Q(author=user) | Q(opponent=user)).count()


def get_user_won_matches_number(user: User) -> int:
    return Confirmation.objects.filter(
        Q(match__winner=user) & ~Q(status=Confirmation.STATUS_PENDING_CONFIRMATION) & ~Q(
            status=Confirmation.STATUS_REJECTED)).count()


def get_user_played_games(user: User) -> list:
    user_games = set(Match.objects.filter(Q(author=user) | Q(opponent=user)).values_list("game__name", flat=True))
    return list(user_games)


def get_user_wins_in_specific_game_number(user: User, game: str) -> int:
    return Confirmation.objects.filter(
        (Q(match__author=user) | Q(match__opponent=user)) & Q(match__winner=user) & Q(match__game__name=game) & Q(
            status=Confirmation.STATUS_CONFIRMED)).count()


def get_user_lost_in_specific_game_number(user: User, game: str) -> int:
    return Confirmation.objects.filter(
        (Q(match__author=user) | Q(match__opponent=user)) & ~Q(match__winner=user) & Q(match__game__name=game) & Q(
            status=Confirmation.STATUS_CONFIRMED)).count()


def get_user_specific_match_pending_confirmation_number(user: User, game: str) -> int:
    return Confirmation.objects.filter(
        (Q(match__author=user) | Q(match__opponent=user)) & Q(match__game__name=game) & Q(
            status=Confirmation.STATUS_PENDING_CONFIRMATION)
    ).count()


def get_user_play_in_specific_game_number(user: User, game: str) -> int:
    return Match.objects.filter((Q(author=user) | Q(opponent=user)) & Q(game__name=game)).count()


def get_user_details_in_each_game(user: User) -> dict:
    game_wins = {}
    user_games = get_user_played_games(user)
    for game in user_games:
        game_wins[game] = {
            "win": get_user_wins_in_specific_game_number(user, game),
            "lost": get_user_lost_in_specific_game_number(user, game),
            "pending": get_user_specific_match_pending_confirmation_number(user, game),
            "all": get_user_play_in_specific_game_number(user, game)
        }
    return game_wins


def get_user_lost_matches_number(user: User) -> int:
    return Confirmation.objects.filter(
        ~Q(match__winner=user) & ~Q(status=Confirmation.STATUS_PENDING_CONFIRMATION)).count()


def get_user_pending_confirmation_matches_number(user: User) -> int:
    return Confirmation.objects.filter(
        (Q(match__author=user) | Q(match__opponent=user)) & Q(status=Confirmation.STATUS_PENDING_CONFIRMATION)
    ).count()


def stats_played_matches(user: User, date_from: None, date_to: None):
    matches = Match.objects.filter(Q(author=user) | Q(opponent=user))
    if date_from:
        matches = matches.filter(date__gte=date_from)
    if date_to:
        matches = matches.filter(date__lte=date_to)
    return matches.count()


def stats_won_matches(user: User, date_from: None, date_to: None):
    won_matches = Confirmation.objects.filter(
        Q(match__winner=user) & ~Q(status=Confirmation.STATUS_PENDING_CONFIRMATION) & ~Q(
            status=Confirmation.STATUS_REJECTED))
    if date_from:
        won_matches = won_matches.filter(match__date__gte=date_from)
    if date_to:
        won_matches = won_matches.filter(match__date__lte=date_to)
    return won_matches.count()


def stats_lost_matches(user: User, date_from: None, date_to: None):
    lost_matches = Confirmation.objects.filter(
        ~Q(match__winner=user) & ~Q(status=Confirmation.STATUS_PENDING_CONFIRMATION))
    if date_from:
        lost_matches = lost_matches.filter(match__date__gte=date_from)
    if date_to:
        lost_matches = lost_matches.filter(match__date__lte=date_to)
    return lost_matches.count()
