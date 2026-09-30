def dashboard_badges(request):
    """Kontador badge ba navbar/sidebar dashboard (mensajen kontaktu seidauk lidu).
    Sé deit kalkula ba utilizador autentikadu, atu labele halo query desnesesáriu
    iha pájina públiku ba visitante anónimu."""
    if not request.user.is_authenticated:
        return {}
    from website.models import ContactMessage
    return {"unread_messages_count": ContactMessage.objects.filter(is_read=False).count()}
