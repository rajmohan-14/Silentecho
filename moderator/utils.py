from django.shortcuts import redirect
from functools import wraps

KINDNESS_THRESHOLD = 50


def is_moderator(session_token: str) -> bool:
   
    from .models import ModRole
    return ModRole.objects.filter(
        session_token=session_token,
        status='active'
    ).exists()


def check_and_nominate(session_token: str):
   
    from .models import ModRole
    from confessions.models import SessionKindness

    # Already in the system
    if ModRole.objects.filter(session_token=session_token).exists():
        return

    # Check kindness points
    try:
        kindness = SessionKindness.objects.get(session_token=session_token)
        if kindness.kindness_points >= KINDNESS_THRESHOLD:
            ModRole.objects.create(
                session_token     = session_token,
                status            = 'candidate',
                kindness_at_grant = kindness.kindness_points,
            )
    except SessionKindness.DoesNotExist:
        pass


def get_mod_role(session_token: str):
    """Returns the ModRole object or None."""
    from .models import ModRole
    try:
        return ModRole.objects.get(session_token=session_token)
    except ModRole.DoesNotExist:
        return None


def mod_required(view_func):
    
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not is_moderator(request.session_token):
            return redirect('mod_unauthorized')
        return view_func(request, *args, **kwargs)
    return wrapper