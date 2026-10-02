"""Views dashboard custom ba app website (Notísia, Artigu, Atividade,
Dokumentu, Programa, Organigrama, Fundador, Parseiru, Slide, Vizaun/Misaun,
Who We Are, Mensajen Kontaktu). Segue padraun: @login_required +
@allowed_users(allowed_roles=[...]), context dict ho group/page/title/legend,
template form_base.html/list_base.html ne'ebe partilhadu."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from config.decorators import allowed_users
from main.crispy import unique_slug
from website.models import (
    NewsPost, NewsImage, Article, Activity, Document,
)
from website.forms import (
    NewsPostForm, NewsImageForm, ArticleForm, ActivityForm, DocumentForm,
)

ROLES = ["admin", "staff"]


def _group(request):
    return request.user.groups.all()[0].name if request.user.groups.exists() else None


# ---------------------------------------------------------------------
# NOTÍSIA (News)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def news_list(request):
    qs = NewsPost.objects.all()
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "news", "title": "Notísia", "legend": "Notísia",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:news-create"),
    }
    return render(request, "dashboard/news_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def news_create(request):
    form = NewsPostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.slug = unique_slug(NewsPost, obj.title)
        obj.save()
        messages.success(request, "Notísia foun kriadu ho susesu.")
        return redirect("main:news-list")
    context = {
        "group": _group(request), "page": "news", "title": "Notísia", "legend": "Foti Notísia Foun",
        "form": form, "list_url": reverse("main:news-list"), "list_label": "Notísia",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def news_update(request, pk):
    obj = get_object_or_404(NewsPost, pk=pk)
    form = NewsPostForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        if not updated.slug:
            updated.slug = unique_slug(NewsPost, updated.title, instance_pk=updated.pk)
        updated.save()
        messages.success(request, "Notísia hadia ona.")
        return redirect("main:news-list")
    context = {
        "group": _group(request), "page": "news", "title": "Notísia", "legend": f"Edita: {obj.title}",
        "form": form, "list_url": reverse("main:news-list"), "list_label": "Notísia",
        "gallery_url": reverse("main:news-gallery", args=[obj.pk]),
    }
    return render(request, "dashboard/news_form.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def news_delete(request, pk):
    obj = get_object_or_404(NewsPost, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Notísia hamoos ona.")
    return redirect("main:news-list")


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def news_gallery(request, pk):
    news = get_object_or_404(NewsPost, pk=pk)
    form = NewsImageForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        img = form.save(commit=False)
        img.news = news
        img.save()
        messages.success(request, "Foto aumenta ona ba galeria.")
        return redirect("main:news-gallery", pk=news.pk)
    context = {
        "group": _group(request), "page": "news", "title": "Galeria Foto",
        "legend": f"Galeria Foto: {news.title}",
        "form": form, "news": news, "images": news.gallery_images.all(),
        "list_url": reverse("main:news-list"), "list_label": "Notísia",
    }
    return render(request, "dashboard/news_gallery.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def news_image_delete(request, pk):
    img = get_object_or_404(NewsImage, pk=pk)
    news_pk = img.news_id
    if request.method == "POST":
        img.delete()
        messages.success(request, "Foto hamoos ona.")
    return redirect("main:news-gallery", pk=news_pk)


# ---------------------------------------------------------------------
# ARTIGU (Article)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def article_list(request):
    qs = Article.objects.select_related("author")
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "article", "title": "Artigu", "legend": "Artigu",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:article-create"),
    }
    return render(request, "dashboard/article_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def article_create(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.author = request.user
        obj.slug = unique_slug(Article, obj.title)
        obj.save()
        messages.success(request, "Artigu foun kriadu ho susesu.")
        return redirect("main:article-list")
    context = {
        "group": _group(request), "page": "article", "title": "Artigu", "legend": "Foti Artigu Foun",
        "form": form, "list_url": reverse("main:article-list"), "list_label": "Artigu",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def article_update(request, pk):
    obj = get_object_or_404(Article, pk=pk)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        if not updated.slug:
            updated.slug = unique_slug(Article, updated.title, instance_pk=updated.pk)
        updated.save()
        messages.success(request, "Artigu hadia ona.")
        return redirect("main:article-list")
    context = {
        "group": _group(request), "page": "article", "title": "Artigu", "legend": f"Edita: {obj.title}",
        "form": form, "list_url": reverse("main:article-list"), "list_label": "Artigu",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def article_delete(request, pk):
    obj = get_object_or_404(Article, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Artigu hamoos ona.")
    return redirect("main:article-list")


# ---------------------------------------------------------------------
# ATIVIDADE (Activity)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def activity_list(request):
    qs = Activity.objects.select_related("municipality")
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "activity", "title": "Atividade", "legend": "Atividade",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:activity-create"),
    }
    return render(request, "dashboard/activity_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def activity_create(request):
    form = ActivityForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Atividade foun kriadu ho susesu.")
        return redirect("main:activity-list")
    context = {
        "group": _group(request), "page": "activity", "title": "Atividade", "legend": "Foti Atividade Foun",
        "form": form, "list_url": reverse("main:activity-list"), "list_label": "Atividade",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def activity_update(request, pk):
    obj = get_object_or_404(Activity, pk=pk)
    form = ActivityForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Atividade hadia ona.")
        return redirect("main:activity-list")
    context = {
        "group": _group(request), "page": "activity", "title": "Atividade", "legend": f"Edita: {obj.title}",
        "form": form, "list_url": reverse("main:activity-list"), "list_label": "Atividade",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def activity_delete(request, pk):
    obj = get_object_or_404(Activity, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Atividade hamoos ona.")
    return redirect("main:activity-list")


# ---------------------------------------------------------------------
# DOKUMENTU (Document)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def document_list(request):
    qs = Document.objects.select_related("category")
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "document", "title": "Dokumentu", "legend": "Dokumentu",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:document-create"),
    }
    return render(request, "dashboard/document_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def document_create(request):
    form = DocumentForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Dokumentu foun kriadu ho susesu.")
        return redirect("main:document-list")
    context = {
        "group": _group(request), "page": "document", "title": "Dokumentu", "legend": "Foti Dokumentu Foun",
        "form": form, "list_url": reverse("main:document-list"), "list_label": "Dokumentu",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def document_update(request, pk):
    obj = get_object_or_404(Document, pk=pk)
    form = DocumentForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Dokumentu hadia ona.")
        return redirect("main:document-list")
    context = {
        "group": _group(request), "page": "document", "title": "Dokumentu", "legend": f"Edita: {obj.title}",
        "form": form, "list_url": reverse("main:document-list"), "list_label": "Dokumentu",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def document_delete(request, pk):
    obj = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Dokumentu hamoos ona.")
    return redirect("main:document-list")
