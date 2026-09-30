import json
from django import template
from django.utils.text import Truncator

register = template.Library()


@register.filter
def i18n_json(obj, field_name):
    """
    Kombina teks default (Tetum, field asli) ho override tradusaun JSON
    (field_name + '_i18n'), fila hanesan string JSON ne'ebe siguru ba
    embed iha atributu HTML (Django auto-escape sei trata aspas).

    Uza: {{ vision_mission|i18n_json:'vision_text' }}
    """
    base_value = getattr(obj, field_name, "") or ""
    overrides = getattr(obj, f"{field_name}_i18n", None) or {}
    data = {"tet": base_value}
    if isinstance(overrides, dict):
        for lang in ("id", "pt", "en"):
            val = overrides.get(lang)
            if val:
                data[lang] = val
    return json.dumps(data, ensure_ascii=False)


@register.filter
def i18n_json_words(obj, arg):
    """
    Hanesan i18n_json maibe ho limite liafuan (word truncation) ba
    kada lian, atu kartu/preview sira nia tetu hanesan deit iha
    lian hotu-hotu.

    Uza: {{ vision_mission|i18n_json_words:"vision_text:20" }}
    """
    field_name, _, count_str = arg.partition(":")
    try:
        count = int(count_str)
    except ValueError:
        count = 20
    base_value = getattr(obj, field_name, "") or ""
    overrides = getattr(obj, f"{field_name}_i18n", None) or {}
    data = {"tet": Truncator(base_value).words(count)}
    if isinstance(overrides, dict):
        for lang in ("id", "pt", "en"):
            val = overrides.get(lang)
            if val:
                data[lang] = Truncator(val).words(count)
    return json.dumps(data, ensure_ascii=False)


@register.filter
def to_json(value):
    """
    Konverte valor Python (dict/list, mis. mission_points, indicators,
    org_structure_items, geo_focus_regions) diretamente ba string JSON,
    ba embed iha atributu data-i18n-list.

    Uza: data-i18n-list="{{ program.indicators|to_json }}"
    """
    return json.dumps(value or {}, ensure_ascii=False)


@register.filter
def reading_time(text):
    """Estimasi tempu lee (menit), baze ba ~200 liafuan/minutu."""
    if not text:
        return 1
    words = len(text.split())
    minutes = max(1, round(words / 200))
    return minutes
