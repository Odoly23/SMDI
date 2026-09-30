from django.apps import AppConfig


class UserConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "User"
    verbose_name = "Utilizador"

    def ready(self):
        import User.signals  # noqa
