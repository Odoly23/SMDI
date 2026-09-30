"""
URL configuration for sismdi project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Mata Dalan Institute - Administrasaun"
admin.site.site_title = "Painel MDI"
admin.site.index_title = "Jestaun Konteudu Website"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('dashboard/', include('Main.urls')),
    path('', include('Website.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
