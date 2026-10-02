"""Views dashboard custom ba dadus lookup/referénsia: Kategoria, Munisípiu,
Postu Administrativu, Tinan. Modelu sira ne'e simples (poucos campos), maibe
tetu CRUD propriu atu sai konsistente ho restu dashboard (crispy + template
partilhadu), la hatudu Django Admin ba staff ne'ebe la teknikus."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from config.decorators import allowed_users
from main.crispy import unique_slug
from custom.models import Category, Municipality, AdministrativePost, Year
from custom.forms import CategoryForm, MunicipalityForm, AdministrativePostForm, YearForm

ROLES = ["admin", "staff"]


def _group(request):
    return request.user.groups.all()[0].name if request.user.groups.exists() else None


# ---------------------------------------------------------------------
# KATEGORIA (Category)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def category_list(request):
    qs = Category.objects.all()
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "category", "title": "Kategoria", "legend": "Kategoria",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:category-create"),
    }
    return render(request, "dashboard/category_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def category_create(request):
    form = CategoryForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.slug = unique_slug(Category, obj.name)
        obj.save()
        messages.success(request, "Kategoria foun kriadu ho susesu.")
        return redirect("main:category-list")
    context = {
        "group": _group(request), "page": "category", "title": "Kategoria", "legend": "Foti Kategoria Foun",
        "form": form, "list_url": reverse("main:category-list"), "list_label": "Kategoria",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def category_update(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    form = CategoryForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        if not updated.slug:
            updated.slug = unique_slug(Category, updated.name, instance_pk=updated.pk)
        updated.save()
        messages.success(request, "Kategoria hadia ona.")
        return redirect("main:category-list")
    context = {
        "group": _group(request), "page": "category", "title": "Kategoria", "legend": f"Edita: {obj.name}",
        "form": form, "list_url": reverse("main:category-list"), "list_label": "Kategoria",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def category_delete(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Kategoria hamoos ona.")
    return redirect("main:category-list")


# ---------------------------------------------------------------------
# MUNISÍPIU (Municipality)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def municipality_list(request):
    qs = Municipality.objects.all()
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "municipality", "title": "Munisípiu", "legend": "Munisípiu",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:municipality-create"),
    }
    return render(request, "dashboard/municipality_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def municipality_create(request):
    form = MunicipalityForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Munisípiu foun kriadu ho susesu.")
        return redirect("main:municipality-list")
    context = {
        "group": _group(request), "page": "municipality", "title": "Munisípiu", "legend": "Foti Munisípiu Foun",
        "form": form, "list_url": reverse("main:municipality-list"), "list_label": "Munisípiu",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def municipality_update(request, pk):
    obj = get_object_or_404(Municipality, pk=pk)
    form = MunicipalityForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Munisípiu hadia ona.")
        return redirect("main:municipality-list")
    context = {
        "group": _group(request), "page": "municipality", "title": "Munisípiu", "legend": f"Edita: {obj.name}",
        "form": form, "list_url": reverse("main:municipality-list"), "list_label": "Munisípiu",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def municipality_delete(request, pk):
    obj = get_object_or_404(Municipality, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Munisípiu hamoos ona.")
    return redirect("main:municipality-list")


# ---------------------------------------------------------------------
# POSTU ADMINISTRATIVU (AdministrativePost)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def adminpost_list(request):
    qs = AdministrativePost.objects.select_related("municipality")
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "adminpost", "title": "Postu Administrativu",
        "legend": "Postu Administrativu",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:adminpost-create"),
    }
    return render(request, "dashboard/adminpost_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def adminpost_create(request):
    form = AdministrativePostForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Postu Administrativu foun kriadu ho susesu.")
        return redirect("main:adminpost-list")
    context = {
        "group": _group(request), "page": "adminpost", "title": "Postu Administrativu",
        "legend": "Foti Postu Foun",
        "form": form, "list_url": reverse("main:adminpost-list"), "list_label": "Postu Administrativu",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def adminpost_update(request, pk):
    obj = get_object_or_404(AdministrativePost, pk=pk)
    form = AdministrativePostForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Postu Administrativu hadia ona.")
        return redirect("main:adminpost-list")
    context = {
        "group": _group(request), "page": "adminpost", "title": "Postu Administrativu",
        "legend": f"Edita: {obj.name}",
        "form": form, "list_url": reverse("main:adminpost-list"), "list_label": "Postu Administrativu",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def adminpost_delete(request, pk):
    obj = get_object_or_404(AdministrativePost, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Postu Administrativu hamoos ona.")
    return redirect("main:adminpost-list")


# ---------------------------------------------------------------------
# TINAN (Year)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def year_list(request):
    qs = Year.objects.all()
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "year", "title": "Tinan", "legend": "Tinan",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:year-create"),
    }
    return render(request, "dashboard/year_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def year_create(request):
    form = YearForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tinan foun kriadu ho susesu.")
        return redirect("main:year-list")
    context = {
        "group": _group(request), "page": "year", "title": "Tinan", "legend": "Foti Tinan Foun",
        "form": form, "list_url": reverse("main:year-list"), "list_label": "Tinan",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def year_update(request, pk):
    obj = get_object_or_404(Year, pk=pk)
    form = YearForm(request.POST or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Tinan hadia ona.")
        return redirect("main:year-list")
    context = {
        "group": _group(request), "page": "year", "title": "Tinan", "legend": f"Edita: {obj.value}",
        "form": form, "list_url": reverse("main:year-list"), "list_label": "Tinan",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def year_delete(request, pk):
    obj = get_object_or_404(Year, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Tinan hamoos ona.")
    return redirect("main:year-list")
