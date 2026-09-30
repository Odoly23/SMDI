from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator

from Custom.models import Category
from .models import (
    Slide, VisionMission, WhoWeAre, Program, Activity,
    NewsPost, Article, OrgMember, Founder, Partner, Document
)
from .forms import ContactMessageForm


def home(request):
    context = {
        "slides": Slide.objects.filter(is_active=True),
        "vision_mission": VisionMission.load(),
        "who_we_are": WhoWeAre.load(),
        # Limit 5 & selalu ambil yang PALING BARU (bukan urutan manual 'order')
        "activities": Activity.objects.filter(is_published=True).order_by("-created_at", "-id")[:5],
        "news_list": NewsPost.objects.filter(is_published=True).order_by("-published_date", "-id")[:5],
        "articles": Article.objects.filter(is_published=True).select_related("author").order_by("-published_date", "-id")[:5],
        "org_top": OrgMember.objects.filter(level=0).prefetch_related("children__children"),
        "partners": Partner.objects.all(),
    }
    return render(request, "Website/index.html", context)


def who_we_are(request):
    context = {
        "who_we_are": WhoWeAre.load(),
        "founders": Founder.objects.all(),
    }
    return render(request, "Website/who_we_are.html", context)


def vision_mission(request):
    context = {"vision_mission": VisionMission.load()}
    return render(request, "Website/vision_mission.html", context)


def what_we_do(request):
    context = {
        "activities": Activity.objects.filter(is_published=True),
        "programs": Program.objects.filter(parent__isnull=True).prefetch_related("children"),
    }
    return render(request, "Website/what_we_do.html", context)


def partners_networks(request):
    context = {"partners": Partner.objects.filter(type="partner")}
    return render(request, "Website/partners_networks.html", context)


def current_donors(request):
    context = {"donors": Partner.objects.filter(type="donor")}
    return render(request, "Website/current_donors.html", context)


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug)
    children = program.children.all()
    all_pillars = Program.objects.filter(parent__isnull=True).prefetch_related("children")
    return render(request, "Website/program_detail.html", {
        "program": program,
        "children": children,
        "all_pillars": all_pillars,
    })


def documents_by_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug, context="document")
    documents = Document.objects.filter(category=category)
    return render(request, "Website/documents.html", {
        "category": category,
        "documents": documents,
    })


def news_list(request):
    posts = NewsPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "Website/news_list.html", {"page_obj": page_obj})


def news_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, is_published=True)
    return render(request, "Website/news_detail.html", {"post": post})


def article_list(request):
    articles = Article.objects.filter(is_published=True).select_related("author")
    paginator = Paginator(articles, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "Website/article_list.html", {"page_obj": page_obj})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, "Website/article_detail.html", {"article": article})


def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensajen haruka ho susesu! Ami sei kontaktu fila fali lalais.")
            return redirect("Website:contact")
    else:
        form = ContactMessageForm()
    return render(request, "Website/contact.html", {"form": form})
