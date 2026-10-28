from django.conf import settings

from .models import Program


def nav_programs(request):
    """Context processor global - lista Pilar (top-level Program) + sub-outcome (children)
    disponivel iha kada pajina hanesan {{ nav_programs }}, ba navbar/footer dropdown.
    Di-cache 5 minutu; otomatis dihapus bainhira Program muda (haree signals.py)."""
    from django.core.cache import cache
    from .signals import NAV_CACHE_KEY
    programs = cache.get(NAV_CACHE_KEY)
    if programs is None:
        programs = list(
            Program.objects.filter(parent__isnull=True)
            .prefetch_related("children")
            .order_by("order")
        )
        for p in programs:
            list(p.children.all())  # materialize prefetch sebelum cache
        cache.set(NAV_CACHE_KEY, programs, 300)
    return {"nav_programs": programs}


def analytics(request):
    """Hatudu ID Google Analytics (GA4) ba template, se defini iha .env."""
    return {
        "GA_MEASUREMENT_ID": getattr(settings, "GA_MEASUREMENT_ID", ""),
        "PUBLIC_DOCUMENTS": getattr(settings, "PUBLIC_DOCUMENTS", False),
    }


def csp_nonce(request):
    """Nonce CSP ba inline <script> iha template publika."""
    return {"csp_nonce": getattr(request, "csp_nonce", "")}


def asset_version(request):
    """?v=<versi> ba file CSS/JS sira, atu browser la uza file tuan depois update."""
    return {"ASSET_V": getattr(settings, "ASSET_VERSION", "1")}
