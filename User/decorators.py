from django.http import HttpResponse
from django.shortcuts import redirect
from functools import wraps


def unauthenticated_user(view_func):
    """Redirect user ne'ebe login ona bainhira hakarak asesu pajina login."""
    @wraps(view_func)
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("Main:home")
        return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_users(allowed_roles=None):
    """
    Decorator ba restrict view tuir Profile.role.
    Uza hanesan: @allowed_users(allowed_roles=['admin', 'editor'])
    """
    allowed_roles = allowed_roles or []

    def decorator(view_func):
        @wraps(view_func)
        def wrapper_func(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("Main:login")
            profile = getattr(request.user, "profile", None)
            if request.user.is_superuser or (profile and profile.role in allowed_roles):
                return view_func(request, *args, **kwargs)
            return HttpResponse("Ita seidauk iha permisaun atu asesu pajina ne'e. (403 Forbidden)", status=403)
        return wrapper_func
    return decorator


def admin_only(view_func):
    return allowed_users(allowed_roles=["admin"])(view_func)
