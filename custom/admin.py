from django.contrib import admin
from .models import Category, Municipality, AdministrativePost, Year


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "context", "slug")
    list_filter = ("context",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class AdministrativePostInline(admin.TabularInline):
    model = AdministrativePost
    extra = 1


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    inlines = [AdministrativePostInline]


@admin.register(Year)
class YearAdmin(admin.ModelAdmin):
    list_display = ("value",)
