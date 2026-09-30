from django.db import models
from django.contrib.auth.models import User

# Grupu ba kontrolu asesu (config.decorators.allowed_users lee husi
# request.user.groups). Uza konstante sira-ne'e iha seed_data/admin
# atu evita hakerek naran grupu ho liman kada fatin.
GROUP_ADMIN = "admin"
GROUP_EDITOR = "editor"
GROUP_AUTHOR = "author"
GROUP_MEMBER = "member"
BACKEND_GROUPS = (GROUP_ADMIN, GROUP_EDITOR, GROUP_AUTHOR)


class Profile(models.Model):
    """Ekstensaun ba Django User default - simpan foto, jabatan, bio.
    Kontrolu asesu/role la simpan iha profile ida-ne'e ona (uza
    django.contrib.auth.models.Group liu husi config.decorators.allowed_users)."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    position = models.CharField(max_length=150, blank=True, help_text="Kargu/jabatan, mis. Peskizador Senior")
    photo = models.ImageField(upload_to="staff/", blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = "Perfil Utilizador"
        verbose_name_plural = "Perfil Utilizador"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"

    @property
    def is_backend_staff(self):
        """True se user iha ona iha grupu admin/editor/author (haree BACKEND_GROUPS)."""
        if self.user.is_superuser:
            return True
        return self.user.groups.filter(name__in=BACKEND_GROUPS).exists()
