"""Views dashboard custom ba Slide Hero (lista normál) no konteúdu singleton
(Vizaun & Misaun, Who We Are, Konfigurasaun Situs - rejistu ida deit, edita
deit, la bele kria/hamoos). Segue padraun hanesan main/views_website.py."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from config.decorators import allowed_users
from config.models import SiteConfig
from config.forms import SiteConfigForm
from website.models import Slide, VisionMission, WhoWeAre
from website.forms import SlideForm, VisionMissionForm, WhoWeAreForm

ROLES = ["admin", "staff"]


def _group(request):
    return request.user.groups.all()[0].name if request.user.groups.exists() else None


# ---------------------------------------------------------------------
# SLIDE HERO (normal list, not a singleton)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def slide_list(request):
    qs = Slide.objects.all()
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "slide", "title": "Slide Hero", "legend": "Slide Hero",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:slide-create"),
    }
    return render(request, "dashboard/slide_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def slide_create(request):
    form = SlideForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Slide foun kriadu ho susesu.")
        return redirect("main:slide-list")
    context = {
        "group": _group(request), "page": "slide", "title": "Slide Hero", "legend": "Foti Slide Foun",
        "form": form, "list_url": reverse("main:slide-list"), "list_label": "Slide Hero",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def slide_update(request, pk):
    obj = get_object_or_404(Slide, pk=pk)
    form = SlideForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Slide hadia ona.")
        return redirect("main:slide-list")
    context = {
        "group": _group(request), "page": "slide", "title": "Slide Hero", "legend": f"Edita: {obj.title}",
        "form": form, "list_url": reverse("main:slide-list"), "list_label": "Slide Hero",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def slide_delete(request, pk):
    obj = get_object_or_404(Slide, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Slide hamoos ona.")
    return redirect("main:slide-list")


# ---------------------------------------------------------------------
# VIZAUN & MISAUN (singleton)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def vision_mission_edit(request):
    obj, _created = VisionMission.objects.get_or_create(pk=1)
    form = VisionMissionForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Vizaun & Misaun hadia ona.")
        return redirect("main:vision-mission-edit")
    context = {
        "group": _group(request), "page": "vision-mission", "title": "Vizaun & Misaun",
        "legend": "Vizaun & Misaun", "form": form,
    }
    return render(request, "layout/form_base.html", context)


# ---------------------------------------------------------------------
# WHO WE ARE (singleton)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def who_we_are_edit(request):
    obj, _created = WhoWeAre.objects.get_or_create(pk=1)
    form = WhoWeAreForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Who We Are hadia ona.")
        return redirect("main:who-we-are-edit")
    context = {
        "group": _group(request), "page": "who-we-are", "title": "Who We Are",
        "legend": "Who We Are", "form": form,
    }
    return render(request, "layout/form_base.html", context)


# ---------------------------------------------------------------------
# KONFIGURASAUN SITUS (SiteConfig - singleton)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def site_config_edit(request):
    obj = SiteConfig.load()
    form = SiteConfigForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Konfigurasaun Situs hadia ona.")
        return redirect("main:site-config-edit")
    context = {
        "group": _group(request), "page": "site-config", "title": "Konfigurasaun Situs",
        "legend": "Konfigurasaun Situs", "form": form,
    }
    return render(request, "layout/form_base.html", context)
