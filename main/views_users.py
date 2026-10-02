"""Views dashboard custom ba jestaun konta Staff (User + Profile + Group).
Deit admin bele asesu (la hanesan ROLES=["admin","staff"] ba restu), tanba
jestaun konta/rola sensitivu - staff la bele troka ninia-an sai admin."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from config.decorators import allowed_users
from users.forms import StaffUserCreateForm, StaffUserUpdateForm

ROLES = ["admin"]


def _group(request):
    return request.user.groups.all()[0].name if request.user.groups.exists() else None


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def staff_list(request):
    qs = User.objects.select_related("profile").prefetch_related("groups").order_by("username")
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "staff", "title": "Konta Staff", "legend": "Konta Staff",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:staff-create"),
    }
    return render(request, "dashboard/staff_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def staff_create(request):
    form = StaffUserCreateForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Konta staff foun kriadu ho susesu.")
        return redirect("main:staff-list")
    context = {
        "group": _group(request), "page": "staff", "title": "Konta Staff", "legend": "Foti Konta Staff Foun",
        "form": form, "list_url": reverse("main:staff-list"), "list_label": "Konta Staff",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def staff_update(request, pk):
    obj = get_object_or_404(User, pk=pk)
    form = StaffUserUpdateForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Konta staff hadia ona.")
        return redirect("main:staff-list")
    context = {
        "group": _group(request), "page": "staff", "title": "Konta Staff",
        "legend": f"Edita: {obj.get_full_name() or obj.username}",
        "form": form, "list_url": reverse("main:staff-list"), "list_label": "Konta Staff",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def staff_delete(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        if obj.pk == request.user.pk:
            messages.error(request, "La bele hamoos ninia-an konta.")
        elif obj.is_superuser:
            messages.error(request, "La bele hamoos konta superuser.")
        else:
            obj.delete()
            messages.success(request, "Konta staff hamoos ona.")
    return redirect("main:staff-list")
