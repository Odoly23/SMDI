from django.contrib import admin
from .models import SiteConfig


@admin.register(SiteConfig)
class SiteConfigAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identitas Situs", {
            "fields": ("site_name", "short_name", "tagline", "logo", "favicon")
        }),
        ("Kontak", {
            "fields": ("email", "phone", "address")
        }),
        ("Lokasi Aktivitas / Peta", {
            "fields": ("activity_location_name", "latitude", "longitude")
        }),
        ("Sosial Media", {
            "fields": ("facebook_url", "blog_url")
        }),
        ("Konten Footer", {
            "fields": ("about_text", "footer_credit")
        }),
        ("Estatístika Vizitante", {
            "fields": ("flagcounter_id",),
            "description": (
                "Widget FlagCounter hatudu bandeira/kontador vizitante tuir nasaun, "
                "iha topbar (besik lingua) no iha footer. Haree help text iha baixu "
                "atu hetan ID ne'e."
            ),
        }),
    )

    def has_add_permission(self, request):
        # Cegah tambah data baru jika singleton sudah ada
        return not SiteConfig.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
