from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache

from config.decorators import allowed_users, unauthenticated_user
from website.models import NewsPost, Article, Activity, ContactMessage, Partner, Document

# Limitasaun tentativa login (brute-force protection) — la depende ba pakote
# terseiru, uza cache framework Django nian deit (default LocMemCache).
LOGIN_MAX_ATTEMPTS = 5
LOGIN_LOCKOUT_SECONDS = 15 * 60  # 15 minutu


def _client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR", "unknown")


def _login_attempts_key(request):
    return f"login_attempts:{_client_ip(request)}"


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        attempts_key = _login_attempts_key(request)
        attempts = cache.get(attempts_key, 0)

        if attempts >= LOGIN_MAX_ATTEMPTS:
            messages.error(
                request,
                "Tentativa login liu demais husi IP ida-ne'e. Favor tenta fali "
                "depois de 15 minutu.",
            )
            return render(request, "home/login.html")

        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            cache.delete(attempts_key)
            auth_login(request, user)
            return redirect("main:home")

        cache.set(attempts_key, attempts + 1, LOGIN_LOCKOUT_SECONDS)
        messages.error(request, "Username ka password sala. Favor tenta fila fali.")
    return render(request, "home/login.html")


@login_required(login_url="main:login")
def logout_view(request):
    auth_logout(request)
    return render(request, "home/logout.html")


@login_required(login_url="main:login")
@allowed_users(allowed_roles=["admin", "staff"])
def home(request):
    group = request.user.groups.all()[0].name
    context = {
        "group": group,
        "page": "home",
        "title": "Dashboard",
        "legend": "Dashboard",
        "total_news": NewsPost.objects.count(),
        "total_articles": Article.objects.count(),
        "total_activities": Activity.objects.count(),
        "total_partners": Partner.objects.count(),
        "total_documents": Document.objects.count(),
        "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
        "recent_messages": ContactMessage.objects.all()[:5],
        "recent_news": NewsPost.objects.all()[:5],
    }
    return render(request, "home/home.html", context)
