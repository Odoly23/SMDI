"""Views dashboard custom ba Parseiru/Doador (Partner) no Kaixa Mensajen
Kontaktu (ContactMessage inbox, read-only - mensajen tama husi formuláriu
kontaktu públiku). Segue padraun hanesan main/views_website.py."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

from config.decorators import allowed_users
from website.models import Partner, ContactMessage
from website.forms import PartnerForm

ROLES = ["admin", "staff"]


def _group(request):
    return request.user.groups.all()[0].name if request.user.groups.exists() else None


# ---------------------------------------------------------------------
# PARSEIRU / DOADOR (Partner)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def partner_list(request):
    qs = Partner.objects.all()
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "partner", "title": "Parseiru", "legend": "Parseiru & Doador",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "create_url": reverse("main:partner-create"),
    }
    return render(request, "dashboard/partner_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def partner_create(request):
    form = PartnerForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Parseiru foun kriadu ho susesu.")
        return redirect("main:partner-list")
    context = {
        "group": _group(request), "page": "partner", "title": "Parseiru", "legend": "Foti Parseiru Foun",
        "form": form, "list_url": reverse("main:partner-list"), "list_label": "Parseiru",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def partner_update(request, pk):
    obj = get_object_or_404(Partner, pk=pk)
    form = PartnerForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Parseiru hadia ona.")
        return redirect("main:partner-list")
    context = {
        "group": _group(request), "page": "partner", "title": "Parseiru", "legend": f"Edita: {obj.name}",
        "form": form, "list_url": reverse("main:partner-list"), "list_label": "Parseiru",
    }
    return render(request, "layout/form_base.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def partner_delete(request, pk):
    obj = get_object_or_404(Partner, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Parseiru hamoos ona.")
    return redirect("main:partner-list")


# ---------------------------------------------------------------------
# KAIXA MENSAJEN KONTAKTU (ContactMessage inbox - read-only)
# ---------------------------------------------------------------------
@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def message_list(request):
    qs = ContactMessage.objects.all()
    page_obj = Paginator(qs, 15).get_page(request.GET.get("page"))
    context = {
        "group": _group(request), "page": "message", "title": "Mensajen Kontaktu", "legend": "Mensajen Kontaktu",
        "page_obj": page_obj, "is_paginated": page_obj.has_other_pages(),
        "unread_count": ContactMessage.objects.filter(is_read=False).count(),
    }
    return render(request, "dashboard/message_list.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def message_detail(request, pk):
    obj = get_object_or_404(ContactMessage, pk=pk)
    if not obj.is_read:
        obj.is_read = True
        obj.save(update_fields=["is_read"])
    context = {
        "group": _group(request), "page": "message", "title": "Mensajen Kontaktu",
        "legend": f"Mensajen husi {obj.name}",
        "message_obj": obj,
        "list_url": reverse("main:message-list"), "list_label": "Mensajen Kontaktu",
    }
    return render(request, "dashboard/message_detail.html", context)


@login_required(login_url="main:login")
@allowed_users(allowed_roles=ROLES)
def message_delete(request, pk):
    obj = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "Mensajen hamoos ona.")
    return redirect("main:message-list")
