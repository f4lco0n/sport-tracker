from .utils import get_user_confirmations_number, get_user_rejected_matches_number


def confirmations_processor(request):
    ctx = {}
    if not request.user.is_anonymous:
        ctx = {"to_confirm": get_user_confirmations_number(request.user),
               "rejected_number": get_user_rejected_matches_number(request.user)}
    return ctx
