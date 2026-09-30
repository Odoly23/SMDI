from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from User.decorators import unauthenticated_user
from Website.models import NewsPost, Article, Activity, ContactMessage, Partner, Document


@unauthenticated_user
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("Main:home")
        messages.error(request, "Username ka password sala. Favor tenta fila fali.")
    return render(request, "Home/login.html")


@login_required(login_url="Main:login")
def logout_view(request):
    auth_logout(request)
    return render(request, "Home/logout.html")


@login_required(login_url="Main:login")
def home(request):
    context = {
        "total_news": NewsPost.objects.count(),
        "total_articles": Article.objects.count(),
        "total_activities": Activity.objects.count(),
        "total_partners": Partner.objects.count(),
        "total_documents": Document.objects.count(),
        "unread_messages": ContactMessage.objects.filter(is_read=False).count(),
        "recent_messages": ContactMessage.objects.all()[:5],
        "recent_news": NewsPost.objects.all()[:5],
    }
    return render(request, "Home/home.html", context)
