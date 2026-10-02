from crispy_forms.helper import FormHelper
from django.utils.text import slugify


def dashboard_helper():
    """FormHelper padraun ba hotu-hotu forms CRUD dashboard — form_tag=False
    tanba template form_base.html ona iha <form method="POST" enctype=...>
    nia rasik iha liur (atu suporta file upload + istilu card/breadcrumb
    konsistente), {% crispy form %} deit renda kampu sira."""
    helper = FormHelper()
    helper.form_tag = False
    return helper


def unique_slug(model, base_text, field="slug", instance_pk=None, max_length=270):
    """Jera slug uniku husi base_text (titulu), hadukur -2/-3/... se ona iha.
    Uza iha forms.py bainhira staff la enxe kampu slug (opsional/la iha iha
    formuláriu), atu staff la presiza hanoin kona-ba URL slug manualmente."""
    base = slugify(base_text)[:max_length]
    slug = base
    i = 2
    qs = model.objects.all()
    if instance_pk:
        qs = qs.exclude(pk=instance_pk)
    while qs.filter(**{field: slug}).exists():
        suffix = f"-{i}"
        slug = f"{base[:max_length - len(suffix)]}{suffix}"
        i += 1
    return slug
