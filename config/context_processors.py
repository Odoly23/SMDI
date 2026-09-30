from .models import SiteConfig


def site_config(request):
    """Context processor global - SiteConfig tersedia di semua template sebagai {{ site_config }}"""
    return {"site_config": SiteConfig.load()}
