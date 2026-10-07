from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from custom.models import Category
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
    return render(request, "website/index.html", context)


def who_we_are(request):
    context = {
        "who_we_are": WhoWeAre.load(),
        "founders": Founder.objects.all(),
    }
    return render(request, "website/who_we_are.html", context)


def vision_mission(request):
    context = {"vision_mission": VisionMission.load()}
    return render(request, "website/vision_mission.html", context)


ACTIVITIES_PER_PAGE = 9


def what_we_do(request):
    """Lista atividade: ringkas (max 100 liafuan), bele buka (q) no filtru tag, ho paginasaun."""
    q = (request.GET.get("q") or "").strip()
    tag = (request.GET.get("tag") or "").strip()
    base = Activity.objects.filter(is_published=True)
    tags = list(base.order_by("tag").values_list("tag", flat=True).distinct())
    activities = base
    if q:
        activities = activities.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(tag__icontains=q)
        )
    if tag:
        activities = activities.filter(tag=tag)
    page_obj = Paginator(activities, ACTIVITIES_PER_PAGE).get_page(request.GET.get("page"))
    # query string tuir mai (la inklui page) ba link paginasaun
    keep = request.GET.copy()
    keep.pop("page", None)
    context = {
        "page_obj": page_obj,
        "activities": page_obj,
        "tags": tags,
        "q": q,
        "active_tag": tag,
        "total": activities.count(),
        "querystring": keep.urlencode(),
        "programs": Program.objects.filter(parent__isnull=True).order_by("order"),
    }
    return render(request, "website/what_we_do.html", context)


def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk, is_published=True)
    others = Activity.objects.filter(is_published=True).exclude(pk=pk)[:3]
    return render(request, "website/activity_detail.html", {"activity": activity, "others": others})


def partners_networks(request):
    context = {"partners": Partner.objects.filter(type="partner")}
    return render(request, "website/partners_networks.html", context)


def current_donors(request):
    context = {"donors": Partner.objects.filter(type="donor")}
    return render(request, "website/current_donors.html", context)


def program_detail(request, slug):
    program = get_object_or_404(Program, slug=slug)
    children = program.children.all()
    all_pillars = Program.objects.filter(parent__isnull=True).prefetch_related("children")
    return render(request, "website/program_detail.html", {
        "program": program,
        "children": children,
        "all_pillars": all_pillars,
    })


def documents_by_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug, context="document")
    documents = Document.objects.filter(category=category)
    return render(request, "website/documents.html", {
        "category": category,
        "documents": documents,
    })


def news_list(request):
    posts = NewsPost.objects.filter(is_published=True)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "website/news_list.html", {"page_obj": page_obj})


def news_detail(request, slug):
    post = get_object_or_404(NewsPost, slug=slug, is_published=True)
    return render(request, "website/news_detail.html", {"post": post})


def article_list(request):
    articles = Article.objects.filter(is_published=True).select_related("author")
    paginator = Paginator(articles, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "website/article_list.html", {"page_obj": page_obj})


def article_detail(request, slug):
    article = get_object_or_404(Article, slug=slug, is_published=True)
    return render(request, "website/article_detail.html", {"article": article})


def contact(request):
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Mensajen haruka ho susesu! Ami sei kontaktu fila fali lalais.")
            return redirect("website:contact")
    else:
        form = ContactMessageForm()
    return render(request, "website/contact.html", {"form": form})
