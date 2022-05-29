from django.contrib.auth.models import User
from django.db.models import Q
from game.models import Confirmation, Match
from datetime import datetime


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


def get_timestamp() -> str:
    timestamp: datetime = datetime.now()
    return timestamp.strftime('%Y-%m/%d-%H%M%S')
