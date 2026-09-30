from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """Ekstensaun ba Django User default - simpan role, foto, no jabatan."""
    ROLE_CHOICES = [
        ("admin", "Administrador"),
        ("editor", "Editor Konteudu"),
        ("author", "Autor / Staff"),
        ("member", "Membru"),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="member")
    position = models.CharField(max_length=150, blank=True, help_text="Kargu/jabatan, mis. Peskizador Senior")
    photo = models.ImageField(upload_to="staff/", blank=True, null=True)
    bio = models.TextField(blank=True)
    phone = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = "Perfil Utilizador"
        verbose_name_plural = "Perfil Utilizador"

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} ({self.get_role_display()})"

    @property
    def is_backend_staff(self):
        return self.role in ("admin", "editor", "author")
