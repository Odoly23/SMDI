from django import forms

from main.crispy import dashboard_helper
from .models import Category, Municipality, AdministrativePost, Year


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "context"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class MunicipalityForm(forms.ModelForm):
    class Meta:
        model = Municipality
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class AdministrativePostForm(forms.ModelForm):
    class Meta:
        model = AdministrativePost
        fields = ["municipality", "name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class YearForm(forms.ModelForm):
    class Meta:
        model = Year
        fields = ["value"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()
