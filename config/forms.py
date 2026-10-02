from django import forms

from main.crispy import dashboard_helper
from .models import SiteConfig


class SiteConfigForm(forms.ModelForm):
    class Meta:
        model = SiteConfig
        fields = [
            "site_name", "short_name", "tagline", "logo", "favicon",
            "email", "phone", "address",
            "activity_location_name", "latitude", "longitude",
            "facebook_url", "blog_url",
            "about_text", "footer_credit", "flagcounter_id",
        ]
        widgets = {
            "about_text": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()
