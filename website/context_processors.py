from django.conf import settings

from .models import Program


def nav_programs(request):
    """Context processor global - lista Pilar (top-level Program) + sub-outcome (children)
    disponivel iha kada pajina hanesan {{ nav_programs }}, ba navbar/footer dropdown."""
    programs = (
        Program.objects.filter(parent__isnull=True)
        .prefetch_related("children")
        .order_by("order")
    )
    return {"nav_programs": programs}


def analytics(request):
    """Hatudu ID Google Analytics (GA4) ba template, se defini iha .env."""
    return {"GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", "")}
