from django.contrib import admin
from .models import (
    Slide, VisionMission, WhoWeAre, Program, Activity,
    NewsPost, NewsImage, Article, OrgMember, Founder, Partner, Document, ContactMessage
)

I18N_HELP = (
    "Kaben JSON ba tradusaun opsional. Se husik mamuk, site sei uza teks Tetum "
    "(azima/default) hanesan fallback ba lian ne'ebe seidauk iha tradusaun. "
    'Formatu: {"id": "Teks Indonesia", "pt": "Teks Portugues", "en": "English text"}'
)


@admin.register(Slide)
class SlideAdmin(admin.ModelAdmin):
    list_display = ("title", "order", "is_active")
    list_editable = ("order", "is_active")
    fieldsets = (
        (None, {"fields": ("kicker", "title", "text", "image", "order", "is_active")}),
        ("Tradusaun (opsional)", {
            "classes": ("collapse",),
            "fields": ("kicker_i18n", "title_i18n", "text_i18n"),
            "description": I18N_HELP,
        }),
    )


@admin.register(VisionMission)
class VisionMissionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("vision_text", "mission_text", "mission_points")}),
        ("Tradusaun (opsional)", {
            "classes": ("collapse",),
            "fields": ("vision_text_i18n", "mission_text_i18n"),
            "description": I18N_HELP,
        }),
    )

    def has_add_permission(self, request):
        return not VisionMission.objects.exists()


@admin.register(WhoWeAre)
class WhoWeAreAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {"fields": ("profile_title", "profile_text", "who_we_are_text",
                            "established_year", "based_in", "focus_area")}),
        ("Tradusaun (opsional)", {
            "classes": ("collapse",),
            "fields": ("profile_text_i18n", "who_we_are_text_i18n"),
            "description": I18N_HELP,
        }),
        ("Estrutura Organizasionál", {
            "fields": ("org_structure_title", "org_structure_intro", "org_structure_items",
                       "org_structure_outro"),
        }),
        ("Estrutura Organizasionál - Tradusaun (opsional)", {
            "classes": ("collapse",),
            "fields": ("org_structure_intro_i18n", "org_structure_outro_i18n"),
            "description": I18N_HELP,
        }),
        ("Abordajen Estratéjiku", {
            "fields": ("strategy_title", "strategy_text"),
        }),
        ("Abordajen Estratéjiku - Tradusaun (opsional)", {
            "classes": ("collapse",),
            "fields": ("strategy_text_i18n",),
            "description": I18N_HELP,
        }),
        ("Foku Jeográfiku", {
            "fields": ("geo_focus_title", "geo_focus_intro", "geo_focus_regions", "geo_focus_outro"),
        }),
        ("Foku Jeográfiku - Tradusaun (opsional)", {
            "classes": ("collapse",),
            "fields": ("geo_focus_intro_i18n", "geo_focus_outro_i18n"),
            "description": I18N_HELP,
        }),
    )

    def has_add_permission(self, request):
        return not WhoWeAre.objects.exists()


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "slug", "order")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("order",)
    list_filter = ("parent",)
    fieldsets = (
        (None, {"fields": ("parent", "title", "slug", "heading", "description", "indicators", "icon", "order")}),
        ("Tradusaun (opsional)", {
            "classes": ("collapse",),
            "fields": ("title_i18n", "heading_i18n", "description_i18n"),
            "description": I18N_HELP,
        }),
    )


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "municipality", "is_published", "order")
    list_editable = ("order", "is_published")
    list_filter = ("is_published", "municipality")
    search_fields = ("title", "tag")


class NewsImageInline(admin.TabularInline):
    model = NewsImage
    extra = 3
    fields = ("image", "caption", "order")


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "municipality", "published_date", "is_published", "gallery_count")
    list_filter = ("is_published", "category", "municipality")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt")
    date_hierarchy = "published_date"
    inlines = [NewsImageInline]
    fieldsets = (
        (None, {"fields": ("title", "slug", "excerpt", "body", "image", "category",
                            "published_date", "is_published")}),
        ("Detalha Data (hanesan Programa)", {
            "fields": ("municipality", "related_program", "location_detail", "source_reference"),
            "description": "Metadata detalladu opsional atu haforsa kontestu notísia ne'e "
                            "(similar ho detalhe iha pájina Programa).",
        }),
    )

    @admin.display(description="Galeria")
    def gallery_count(self, obj):
        return obj.gallery_images.count()


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "category", "published_date", "is_published")
    list_filter = ("is_published", "category", "author")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "excerpt")
    date_hierarchy = "published_date"
    fields = ("title", "slug", "excerpt", "cover_image", "body", "author", "category",
              "published_date", "is_published")


@admin.register(OrgMember)
class OrgMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "parent", "level", "order")
    list_editable = ("order",)
    list_filter = ("level",)


@admin.register(Founder)
class FounderAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "order")
    list_editable = ("order",)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "order")
    list_editable = ("order",)
    list_filter = ("type",)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "published_date")
    list_filter = ("category",)
    date_hierarchy = "published_date"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "message", "created_at")
