from django.db import models
from django.core.exceptions import ValidationError


class SiteConfig(models.Model):
    """
    Konfigurasi global situs (singleton - hanya boleh ada 1 baris data).
    Diakses di seluruh template lewat context processor config.context_processors.site_config
    """
    site_name = models.CharField(max_length=150, default="Mata Dalan Institute")
    short_name = models.CharField(max_length=20, default="MDI")
    tagline = models.CharField(
        max_length=200,
        default="Monitoring . Advocacy . Community Strengthening"
    )
    logo = models.ImageField(upload_to="config/", blank=True, null=True)
    favicon = models.ImageField(upload_to="config/", blank=True, null=True)

    email = models.EmailField(default="info@mditl.org")
    phone = models.CharField(max_length=30, default="+670 7845 9090")
    address = models.CharField(max_length=255, default="Bebonuk, Comoro, Dili, Timor-Leste")

    activity_location_name = models.CharField(max_length=255, default="Tasi Tolu, Dili, Timor-Leste")
    latitude = models.DecimalField(max_digits=15, decimal_places=12, default=-8.563037754273)
    longitude = models.DecimalField(max_digits=15, decimal_places=12, default=125.501539777895)

    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/matadalaninstitute/")
    blog_url = models.URLField(blank=True, default="https://matadalaninstitute.blogspot.com/")

    about_text = models.TextField(
        default="Institute For Monitoring, Advocacy And Community Strengthening - "
                "organizasaun naun-governamentál (ONG) ne'ebe harii iha Timor-Leste "
                "dezde tinan 2005."
    )
    footer_credit = models.CharField(
        max_length=255,
        default="Site ne'e dezenvolve ho Bootstrap 5 & Django."
    )

    flagcounter_id = models.CharField(
        max_length=20, blank=True,
        verbose_name="FlagCounter ID",
        help_text=(
            "ID kontador husi flagcounter.com — halo konta gratis iha "
            "https://flagcounter.com/ (klik \"Get your free counter!\"), "
            "kopia deit ID ne'ebe mosu iha URL imajen (mis. husi "
            "https://s11.flagcounter.com/count2/<b>abcd</b>/... ID = \"abcd\"). "
            "Se mamuk, widget visitante-per-nasaun la hatudu iha site."
        ),
    )

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Konfigurasaun Situs"
        verbose_name_plural = "Konfigurasaun Situs"

    def clean(self):
        if not self.pk and SiteConfig.objects.exists():
            raise ValidationError("Konfigurasaun situs ona iha ona - edita mesak deit rejistu ne'ebe eziste.")

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # Singleton tidak boleh dihapus

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return self.site_name
