"""Views dashboard custom ba estrutura organizasaun: Programa (Pilar/Sub-Outcome),
Organigrama (OrgMember), Fundador (Founder). Segue padraun ne'ebe hanesan
main/views_website.py: @login_required + @allowed_users, context dict ho
group/page/title/legend, template form_base.html/list_base.html partilhadu."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from config.decorators import allowed_users
from main.crispy import unique_slug
from website.models import Program, OrgMember, Founder
from website.forms import ProgramForm, OrgMemberForm, FounderForm

ROLES = ["admin", "staff"]


def _group(request):
    return request.user.groups.all()[0].name if request.user.groups.exists() else None


# ---------------------------------------------------------------------
# PROGRAMA (Pilar / Sub-Outcome)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def program_list(request):
    qs = Program.objects.select_related("parent")
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "program", "title": "Programa", "legend": "Programa",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:program-create"),
    }
    return render(request, "dashboard/program_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def program_create(request):
    form = ProgramForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        obj = form.save(commit=False)
        obj.slug = unique_slug(Program, obj.title)
        obj.save()
        messages.success(request, "Programa foun kriadu ho susesu.")
        return redirect("main:program-list")
    context = {
        "group": _group(request), "page": "program", "title": "Programa", "legend": "Foti Programa Foun",
        "form": form, "list_url": reverse("main:program-list"), "list_label": "Programa",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def program_update(request, pk):
    obj = get_object_or_404(Program, pk=pk)
    form = ProgramForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        updated = form.save(commit=False)
        if not updated.slug:
            updated.slug = unique_slug(Program, updated.title, instance_pk=updated.pk)
        updated.save()
        messages.success(request, "Programa hadia ona.")
        return redirect("main:program-list")
    context = {
        "group": _group(request), "page": "program", "title": "Programa", "legend": f"Edita: {obj.title}",
        "form": form, "list_url": reverse("main:program-list"), "list_label": "Programa",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def program_delete(request, pk):
    obj = get_object_or_404(Program, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Programa hamoos ona.")
    return redirect("main:program-list")


# ---------------------------------------------------------------------
# ORGANIGRAMA (OrgMember)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def orgmember_list(request):
    qs = OrgMember.objects.select_related("parent")
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "orgmember", "title": "Organigrama", "legend": "Organigrama",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:orgmember-create"),
    }
    return render(request, "dashboard/orgmember_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def orgmember_create(request):
    form = OrgMemberForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Membru Organigrama foun kriadu ho susesu.")
        return redirect("main:orgmember-list")
    context = {
        "group": _group(request), "page": "orgmember", "title": "Organigrama", "legend": "Foti Membru Foun",
        "form": form, "list_url": reverse("main:orgmember-list"), "list_label": "Organigrama",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def orgmember_update(request, pk):
    obj = get_object_or_404(OrgMember, pk=pk)
    form = OrgMemberForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Membru Organigrama hadia ona.")
        return redirect("main:orgmember-list")
    context = {
        "group": _group(request), "page": "orgmember", "title": "Organigrama", "legend": f"Edita: {obj.name}",
        "form": form, "list_url": reverse("main:orgmember-list"), "list_label": "Organigrama",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def orgmember_delete(request, pk):
    obj = get_object_or_404(OrgMember, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Membru Organigrama hamoos ona.")
    return redirect("main:orgmember-list")


# ---------------------------------------------------------------------
# FUNDADOR (Founder)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def founder_list(request):
    qs = Founder.objects.all()
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "founder", "title": "Fundador", "legend": "Fundador",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:founder-create"),
    }
    return render(request, "dashboard/founder_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def founder_create(request):
    form = FounderForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fundador foun kriadu ho susesu.")
        return redirect("main:founder-list")
    context = {
        "group": _group(request), "page": "founder", "title": "Fundador", "legend": "Foti Fundador Foun",
        "form": form, "list_url": reverse("main:founder-list"), "list_label": "Fundador",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def founder_update(request, pk):
    obj = get_object_or_404(Founder, pk=pk)
    form = FounderForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Fundador hadia ona.")
        return redirect("main:founder-list")
    context = {
        "group": _group(request), "page": "founder", "title": "Fundador", "legend": f"Edita: {obj.name}",
        "form": form, "list_url": reverse("main:founder-list"), "list_label": "Fundador",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def founder_delete(request, pk):
    obj = get_object_or_404(Founder, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Fundador hamoos ona.")
    return redirect("main:founder-list")
