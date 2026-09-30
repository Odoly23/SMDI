from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from config.decorators import allowed_users, unauthenticated_user
from website.models import NewsPost, Article, Activity, ContactMessage, Partner, Document


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("main:home")
        messages.error(request, "Username ka password sala. Favor tenta fila fali.")
    return render(request, "home/login.html")


@login_required(login_url="main:login")
def logout_view(request):
    auth_logout(request)
    return render(request, "home/logout.html")


@login_required(login_url="main:login")
@allowed_users(allowed_roles=["admin", "editor", "author"])
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
