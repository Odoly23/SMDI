from django.core.cache import cache
from django.http import HttpResponseForbidden

# Limitasaun tentativa login iha nivel middleware — cobre HOTU login form
# (dashboard custom /dashboard/login/ NO Django Admin /admin/login/), atu
# ataker labele halai husi throttle iha main/views.py hodi ataka /admin/
# diretamente. Uza IP + caminho hanesan xave, cache framework Django nian
# deit (haree CACHES iha settings.py).
#
# Konta deit tentativa FALHA (response la halo redirect 3xx) — atu la
# bloke utilizador lejítimu sira ne'ebe hela iha IP hanesan (eskritóriu)
# bainhira ida-idak sira halo login ho susesu.
LOGIN_PATHS = ("/dashboard/login/", "/admin/login/")
MAX_ATTEMPTS = 10
WINDOW_SECONDS = 15 * 60


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


class LoginRateLimitMiddleware:
    """Bloke tentativa login POST bainhira tentativa FALHA liu husi
    MAX_ATTEMPTS husi IP ida iha WINDOW_SECONDS. Response bloke: 403 simples
    (laos template) atu la fó informasaun adisional ba ataker."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        is_login_post = request.method == "POST" and request.path in LOGIN_PATHS
        key = f"login_rl:{_client_ip(request)}" if is_login_post else None

        if is_login_post:
            attempts = cache.get(key, 0)
            if attempts >= MAX_ATTEMPTS:
                return HttpResponseForbidden(
                    "Tentativa login liu demais. Favor tenta fali depois de 15 minutu."
                )

        response = self.get_response(request)

        if is_login_post:
            # Redirect (3xx) hanesan sinál susesu (Django Admin no login:home
            # hotu-hotu redireciona bainhira susesu) — reset kontador.
            if 300 <= response.status_code < 400:
                cache.delete(key)
            else:
                cache.set(key, cache.get(key, 0) + 1, WINDOW_SECONDS)

        return response
