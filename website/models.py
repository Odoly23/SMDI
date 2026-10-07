from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from custom.models import Category, Municipality


# =====================================================================
# HERO SLIDER
# =====================================================================
class Slide(models.Model):
    kicker = models.CharField(max_length=150, help_text="Teks kecil di atas judul (bahasa Tetum, default)")
    title = models.CharField(max_length=200)
    text = models.CharField(max_length=300)
    image = models.ImageField(upload_to="website/slides/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    # Tradusaun opsional ba id/pt/en. Formatu: {"id": "...", "pt": "...", "en": "..."}
    # Se fila mamuk, site sei uza teks Tetum azima hanesan fallback.
    kicker_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')
    title_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')
    text_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')

    class Meta:
        ordering = ["order"]
        verbose_name = "Slide Hero"
        verbose_name_plural = "Slide Hero"

    def __str__(self):
        return self.title


# =====================================================================
# VISION / MISSION / WHO WE ARE / CHAIRMAN (singleton-style content)
# =====================================================================
class VisionMission(models.Model):
    vision_text = models.TextField(help_text="Teks default (Tetum)")
    mission_text = models.TextField(help_text="Teks default (Tetum), uza se mission_points mamuk")
    vision_text_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')
    mission_text_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')
    mission_points = models.JSONField(
        default=dict, blank=True,
        help_text='Lista misaun per lian: {"tet": ["...", "..."], "id": [...], "pt": [...], "en": [...]}'
    )

    class Meta:
        verbose_name = "Vizaun & Misaun"
        verbose_name_plural = "Vizaun & Misaun"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            "vision_text": "Sosiedade Timor-Leste ne'ebe justu, transparente no partisipativu.",
            "mission_text": "Halo monitorizasaun independente, advokasia baze-evidensia no haforsa komunidade.",
        })
        return obj

    def __str__(self):
        return "Vizaun & Misaun MDI"


class WhoWeAre(models.Model):
    profile_title = models.CharField(max_length=150, default="Profile")
    profile_text = models.TextField(help_text="Teks default (Tetum)")
    who_we_are_text = models.TextField(help_text="Teks default (Tetum)")
    profile_text_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')
    who_we_are_text_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')
    established_year = models.CharField(max_length=10, default="2005")
    based_in = models.CharField(max_length=150, default="Bebonuk, Comoro, Dili, Timor-Leste")
    focus_area = models.CharField(max_length=200, default="Monitoring, Advocacy & Community Strengthening")

    # ---- Organizational Structure ----
    org_structure_title = models.CharField(max_length=150, default="Estrutura Organizasionál", blank=True)
    org_structure_intro = models.TextField(blank=True, help_text="Teks default (Tetum)")
    org_structure_intro_i18n = models.JSONField(default=dict, blank=True)
    org_structure_items = models.JSONField(
        default=dict, blank=True,
        help_text='Lista bullet per lian: {"tet": ["...", ...], "id": [...], "pt": [...], "en": [...]}'
    )
    org_structure_outro = models.TextField(blank=True, help_text="Teks default (Tetum)")
    org_structure_outro_i18n = models.JSONField(default=dict, blank=True)

    # ---- Strategic Approach ----
    strategy_title = models.CharField(max_length=150, default="Abordajen Estratéjiku", blank=True)
    strategy_text = models.TextField(blank=True, help_text="Teks default (Tetum)")
    strategy_text_i18n = models.JSONField(default=dict, blank=True)

    # ---- Geographical Focus ----
    geo_focus_title = models.CharField(max_length=150, default="Foku Jeográfiku", blank=True)
    geo_focus_intro = models.TextField(blank=True, help_text="Teks default (Tetum)")
    geo_focus_intro_i18n = models.JSONField(default=dict, blank=True)
    geo_focus_regions = models.JSONField(
        default=dict, blank=True,
        help_text='Lista rejiaun per lian: {"tet": ["Dili", "Viqueque", ...], "id": [...], "pt": [...], "en": [...]}'
    )
    geo_focus_outro = models.TextField(blank=True, help_text="Teks default (Tetum)")
    geo_focus_outro_i18n = models.JSONField(default=dict, blank=True)

    class Meta:
        verbose_name = "Ita Se (Who We Are)"
        verbose_name_plural = "Ita Se (Who We Are)"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1, defaults={
            "profile_text": "MDI mak Organizasaun Naun-Governamentál (ONG) ne'ebe harii iha tinan 2005.",
            "who_we_are_text": "Ekipa peskizador, ativista no fasilitador komunidade.",
        })
        return obj

    def __str__(self):
        return "Ita Se / Profile MDI"


# =====================================================================
# PROGRAM
# =====================================================================
class Program(models.Model):
    """Estrutura Programa MDI: Pilar (top-level, parent=None) + Sub-Outcome (parent=Pilar).
    Mis: Pilar 2 (Think Tank ASEAN) iha 4 sub-outcome: 2.1, 2.2, 2.3, 2.4."""
    title = models.CharField(max_length=150, help_text="Label badak ba menu (Tetum, default)")
    title_i18n = models.JSONField(default=dict, blank=True, help_text='Label menu: {"id":"..","pt":"..","en":".."}')
    slug = models.SlugField(unique=True)
    heading = models.CharField(max_length=250, help_text="Título kompletu (Tetum, default)")
    description = models.TextField(help_text="Teks default (Tetum)")
    heading_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')
    description_i18n = models.JSONField(default=dict, blank=True, help_text='Tradusaun: {"id":"..","pt":"..","en":".."}')
    indicators = models.JSONField(
        default=dict, blank=True,
        help_text='Indikadór Esperadu per lian: {"tet": ["...", ...], "id": [...], "pt": [...], "en": [...]}'
    )
    icon = models.CharField(max_length=50, default="bi-diagram-3", help_text="Nome klase ikon Bootstrap Icons")
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="children",
        help_text="Hela mamuk ba Pilar (top-level). Hili Pilar-inan ba sub-outcome (mis. 2.1, 2.2...)."
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Programa"
        verbose_name_plural = "Programa"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("website:program_detail", kwargs={"slug": self.slug})


# =====================================================================
# ACTIVITY
# =====================================================================
class Activity(models.Model):
    tag = models.CharField(max_length=80)
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to="website/activities/", blank=True, null=True)
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="Urutan tampil manual di halaman 'What We Do' (semua aktivitas)")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Dipakai untuk menentukan aktivitas terbaru di homepage")
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "-id"]
        verbose_name = "Atividade"
        verbose_name_plural = "Atividade"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("website:activity_detail", kwargs={"pk": self.pk})


# =====================================================================
# NEWS
# =====================================================================
class NewsPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True)
    excerpt = models.CharField(max_length=300)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="website/news/", blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True,
                                  limit_choices_to={"context": "news"})
    # Detail data tambahan (hanesan ne'ebe iha Programa): lokasaun no programa relasionadu
    municipality = models.ForeignKey(Municipality, on_delete=models.SET_NULL, blank=True, null=True,
                                      help_text="Munisípiu ne'ebe relasiona ho notísia ne'e")
    related_program = models.ForeignKey("Program", on_delete=models.SET_NULL, blank=True, null=True,
                                         related_name="related_news",
                                         help_text="Programa ne'ebe relasiona (mis. PNDS)")
    location_detail = models.CharField(max_length=200, blank=True,
                                        help_text="Detalhe lokasaun espesífiku, mis. 'Suku Guiço, Postu Same'")
    source_reference = models.CharField(max_length=200, blank=True,
                                         help_text="Referénsia/fonte orijinál (opsional)")
    published_date = models.DateField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "Notisia"
        verbose_name_plural = "Notisia"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("website:news_detail", kwargs={"slug": self.slug})


class NewsImage(models.Model):
    """Galeria foto - satu NewsPost bele iha foto barak (banyak foto untuk satu berita)."""
    news = models.ForeignKey(NewsPost, on_delete=models.CASCADE, related_name="gallery_images")
    image = models.ImageField(upload_to="website/news_gallery/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Foto Galeria Notísia"
        verbose_name_plural = "Foto Galeria Notísia"

    def __str__(self):
        return f"Foto - {self.news.title}"
# =====================================================================
# ARTICLE (written by staff/authors)
# =====================================================================
class Article(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=270, unique=True)
    excerpt = models.CharField(max_length=300)
    body = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to="website/articles/", blank=True, null=True,
                                     help_text="Foto sampul artigu (opsional, hasoru tampilan liu diak)")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True,
                                  limit_choices_to={"context": "article"})
    published_date = models.DateField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "Artigu"
        verbose_name_plural = "Artigu"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("website:article_detail", kwargs={"slug": self.slug})


# =====================================================================
# ORGANIZATIONAL CHART (struktur jabatan/hierarquia internu, opsional)
# =====================================================================
class OrgMember(models.Model):
    name = models.CharField(max_length=150)
    position = models.CharField(max_length=150)
    photo = models.ImageField(upload_to="website/org/", blank=True, null=True)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, related_name="children")
    level = models.PositiveIntegerField(default=0, help_text="0 = puncak/Diretor Ezekutivu")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["level", "order"]
        verbose_name = "Membru Organigrama"
        verbose_name_plural = "Organigrama"

    def __str__(self):
        return f"{self.name} - {self.position}"


# =====================================================================
# FUNDADOR (Founders) - grid pendiri MDI, bukan hierarquia
# =====================================================================
class Founder(models.Model):
    name = models.CharField(max_length=150, help_text="Mis. Sr. Estevanus Coli")
    position = models.CharField(
        max_length=200,
        help_text="Kargu/jabatan atuál, mis. 'Actual Director MDI' ka 'Prezidente Koperativa FUNAMOR'"
    )
    photo = models.ImageField(upload_to="website/founders/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]
        verbose_name = "Fundador"
        verbose_name_plural = "Fundador (Founders)"

    def __str__(self):
        return f"{self.name} - {self.position}"


# =====================================================================
# PARTNERS / DONORS
# =====================================================================
class Partner(models.Model):
    TYPE_CHOICES = [
        ("partner", "Parseiru"),
        ("donor", "Doador"),
    ]
    name = models.CharField(max_length=200)
    logo = models.ImageField(upload_to="website/partners/", blank=True, null=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="partner")
    description = models.CharField(max_length=255, blank=True)
    website_url = models.URLField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["type", "order"]
        verbose_name = "Parseiru / Doador"
        verbose_name_plural = "Parseiru / Doador"

    def __str__(self):
        return self.name


# =====================================================================
# DOCUMENTS
# =====================================================================
class Document(models.Model):
    title = models.CharField(max_length=250)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                  limit_choices_to={"context": "document"}, related_name="documents")
    file = models.FileField(upload_to="website/documents/")
    published_date = models.DateField()

    class Meta:
        ordering = ["-published_date"]
        verbose_name = "Dokumentu"
        verbose_name_plural = "Dokumentu"

    def __str__(self):
        return self.title


# =====================================================================
# CONTACT MESSAGE (dari form kontak publik)
# =====================================================================
class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Mensajen Kontaktu"
        verbose_name_plural = "Mensajen Kontaktu"

    def __str__(self):
        return f"{self.name} <{self.email}>"
