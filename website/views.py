from django.conf import settings
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q

from custom.models import Category
from .models import (
    Slide, VisionMission, WhoWeAre, Program, Activity,
    NewsPost, Article, OrgMember, Founder, Partner, Document, ImpactStat
)
from .geo import centroid_for
from .forms import ContactMessageForm


def impact_context():
    """Angka dampak: pakai ImpactStat manual (admin) se iha; se la iha, uza kontajen otomátiku husi database.
    Mapa: munisípiu ho atividade publika no koordenadanian."""
    published = Activity.objects.filter(is_published=True)
    manual = list(ImpactStat.objects.filter(is_active=True))
    if manual:
        stats = [{"obj": m, "label": m.label, "value": m.value, "suffix": m.suffix, "icon": m.icon} for m in manual]
    else:
        stats = [
            {"obj": None, "label": "Atividade", "key": "activities", "value": published.count(), "suffix": "", "icon": "bi-activity"},
            {"obj": None, "label": "Munisípiu", "key": "municipalities", "value": published.exclude(municipality__isnull=True).values("municipality").distinct().count(), "suffix": "", "icon": "bi-geo-alt"},
            {"obj": None, "label": "Notísia", "key": "news", "value": NewsPost.objects.filter(is_published=True).count(), "suffix": "", "icon": "bi-newspaper"},
            {"obj": None, "label": "Parseiru", "key": "partners", "value": Partner.objects.count(), "suffix": "", "icon": "bi-people"},
        ]
        stats = [s for s in stats if s["value"] > 0]
    points = []
    rows = published.exclude(municipality__isnull=True).values("municipality__name").annotate(n=Count("id")).order_by("-n")
    for r in rows:
        c = centroid_for(r["municipality__name"])
        if c:
            points.append({"name": r["municipality__name"], "count": r["n"], "lat": c[0], "lng": c[1]})
    return {"impact_stats": stats, "impact_points": points}


def home(request):
    context = {
        **impact_context(),
        "slides": Slide.objects.filter(is_active=True),
        "vision_mission": VisionMission.load(),
        "who_we_are": WhoWeAre.load(),
        # Limit 5 & selalu ambil yang PALING BARU (bukan urutan manual 'order')
        "activities": Activity.objects.filter(is_published=True).order_by("-created_at", "-id")[:5],
        "news_list": NewsPost.objects.filter(is_published=True).order_by("-published_date", "-id")[:5],
        "articles": Article.objects.filter(is_published=True).select_related("author", "author__profile").order_by("-published_date", "-id")[:5],
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
    mun = (request.GET.get("mun") or "").strip()
    base = Activity.objects.filter(is_published=True)
    tags = list(base.order_by("tag").values_list("tag", flat=True).distinct())
    activities = base
    if q:
        activities = activities.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(tag__icontains=q)
        )
    if tag:
        activities = activities.filter(tag=tag)
    if mun:
        activities = activities.filter(municipality__name=mun)
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
        "active_mun": mun,
        "total": activities.count(),
        "querystring": keep.urlencode(),
        "programs": Program.objects.filter(parent__isnull=True).order_by("order"),
    }
    return render(request, "website/what_we_do.html", context)


def activity_detail(request, pk):
    activity = get_object_or_404(Activity, pk=pk, is_published=True)
    ordered = list(Activity.objects.filter(is_published=True).only("pk", "title", "tag", "image", "order"))
    ids = [a.pk for a in ordered]
    i = ids.index(activity.pk) if activity.pk in ids else 0
    prev_activity = ordered[i - 1] if i > 0 else None
    next_activity = ordered[i + 1] if i + 1 < len(ordered) else None
    others = [a for a in ordered if a.pk != activity.pk][:4]
    words = len(activity.description.split())
    return render(request, "website/activity_detail.html", {
        "activity": activity, "others": others,
        "prev_activity": prev_activity, "next_activity": next_activity,
        "read_minutes": max(1, round(words / 200)),
    })


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
    if not getattr(settings, "PUBLIC_DOCUMENTS", False):
        raise Http404("Dokumen la publiku")
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
    articles = Article.objects.filter(is_published=True).select_related("author", "author__profile")
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


def error_404(request, exception=None):
    return render(request, "404.html", status=404)


def error_500(request):
    """Standalone: la uza context processor/database, atu bele hatudu maske sistema iha problema."""
    from django.http import HttpResponseServerError
    from django.template.loader import render_to_string
    return HttpResponseServerError(render_to_string("500.html"))
