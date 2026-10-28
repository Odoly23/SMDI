from django.apps import apps
from django.core.cache import cache
from django.db.models import ImageField
from django.db.models.signals import post_delete, post_save, pre_save

from .images import optimize_upload

NAV_CACHE_KEY = "nav_programs_v1"


def _optimize_images(sender, instance, **kwargs):
    for f in sender._meta.get_fields():
        if isinstance(f, ImageField):
            optimize_upload(getattr(instance, f.name, None))


def _clear_nav_cache(sender, **kwargs):
    cache.delete(NAV_CACHE_KEY)


def connect():
    for model in list(apps.get_app_config("website").get_models()) + [apps.get_model("users", "Profile")]:
        if any(isinstance(f, ImageField) for f in model._meta.get_fields()):
            pre_save.connect(_optimize_images, sender=model, dispatch_uid=f"optimize_{model.__name__}")
    Program = apps.get_model("website", "Program")
    post_save.connect(_clear_nav_cache, sender=Program, dispatch_uid="nav_cache_save")
    post_delete.connect(_clear_nav_cache, sender=Program, dispatch_uid="nav_cache_delete")
