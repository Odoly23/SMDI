from django import template

from website.images import thumb_url

register = template.Library()


@register.filter
def thumb(field_file, width=600):
    """{{ obj.image|thumb:600 }} -> URL thumbnail WebP (fallback: URL asli)."""
    try:
        width = int(width)
    except (TypeError, ValueError):
        width = 600
    return thumb_url(field_file, width)
