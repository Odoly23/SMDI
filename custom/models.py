from django.db import models


class Category(models.Model):
    """Kategori umum, dipakai lintas app (News, Article, Document, Activity)."""
    CONTEXT_CHOICES = [
        ("news", "Notisia"),
        ("article", "Artigu"),
        ("document", "Dokumentu"),
        ("activity", "Atividade"),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=110, unique=True)
    context = models.CharField(max_length=20, choices=CONTEXT_CHOICES, default="news")

    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategoria"
        ordering = ["context", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_context_display()})"


class Municipality(models.Model):
    """Munisipiu iha Timor-Leste (dipaka ba tag lokasaun programa/aktividade)."""
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Munisípiu"
        verbose_name_plural = "Munisípiu"
        ordering = ["name"]

    def __str__(self):
        return self.name


class AdministrativePost(models.Model):
    """Postu Administrativu, nia parte husi Munisípiu."""
    municipality = models.ForeignKey(Municipality, on_delete=models.CASCADE, related_name="posts")
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Postu Administrativu"
        verbose_name_plural = "Postu Administrativu"
        unique_together = ("municipality", "name")
        ordering = ["municipality__name", "name"]

    def __str__(self):
        return f"{self.name}, {self.municipality.name}"


class Year(models.Model):
    """Tinan fiskal/atividade — dipaka ba filter dokumentu/relatoriu."""
    value = models.PositiveIntegerField(unique=True)

    class Meta:
        verbose_name = "Tinan"
        verbose_name_plural = "Tinan"
        ordering = ["-value"]

    def __str__(self):
        return str(self.value)
