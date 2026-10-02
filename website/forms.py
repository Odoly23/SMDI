from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from main.crispy import dashboard_helper
from custom.models import Category
from .models import (
    ContactMessage, Slide, VisionMission, WhoWeAre, Program, Activity,
    NewsPost, NewsImage, Article, OrgMember, Founder, Partner, Document,
)


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            "name",
            "email",
            "message",
            Submit("submit", "Haruka Mensajen", css_class="btn-mdi-primary w-100"),
        )


# =====================================================================
# Forms dashboard custom (crispy, form_tag=False — haree main/crispy.py)
# =====================================================================

class SlideForm(forms.ModelForm):
    class Meta:
        model = Slide
        fields = ["kicker", "title", "text", "image", "order", "is_active"]
        widgets = {"text": forms.Textarea(attrs={"rows": 3})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class VisionMissionForm(forms.ModelForm):
    class Meta:
        model = VisionMission
        fields = ["vision_text", "mission_text"]
        widgets = {
            "vision_text": forms.Textarea(attrs={"rows": 4}),
            "mission_text": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class WhoWeAreForm(forms.ModelForm):
    class Meta:
        model = WhoWeAre
        fields = [
            "profile_title", "profile_text", "who_we_are_text",
            "established_year", "based_in", "focus_area",
            "org_structure_title", "org_structure_intro", "org_structure_outro",
            "strategy_title", "strategy_text",
            "geo_focus_title", "geo_focus_intro", "geo_focus_outro",
        ]
        widgets = {
            "profile_text": forms.Textarea(attrs={"rows": 4}),
            "who_we_are_text": forms.Textarea(attrs={"rows": 4}),
            "org_structure_intro": forms.Textarea(attrs={"rows": 3}),
            "org_structure_outro": forms.Textarea(attrs={"rows": 3}),
            "strategy_text": forms.Textarea(attrs={"rows": 4}),
            "geo_focus_intro": forms.Textarea(attrs={"rows": 3}),
            "geo_focus_outro": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ["parent", "title", "heading", "description", "icon", "order"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
        labels = {"parent": "Pilar Inan (mamuk se ida-ne'e Pilar foun)"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].queryset = Program.objects.filter(parent__isnull=True)
        if self.instance.pk:
            self.fields["parent"].queryset = self.fields["parent"].queryset.exclude(pk=self.instance.pk)
        self.helper = dashboard_helper()


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ["tag", "title", "description", "image", "municipality", "order", "is_published"]
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = [
            "title", "excerpt", "body", "image", "category",
            "municipality", "related_program", "location_detail", "source_reference",
            "published_date", "is_published",
        ]
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 2}),
            "body": forms.Textarea(attrs={"rows": 8}),
            "published_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(context="news")
        self.helper = dashboard_helper()


class NewsImageForm(forms.ModelForm):
    class Meta:
        model = NewsImage
        fields = ["image", "caption", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["title", "excerpt", "body", "cover_image", "category", "published_date", "is_published"]
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 2}),
            "body": forms.Textarea(attrs={"rows": 8}),
            "published_date": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(context="article")
        self.helper = dashboard_helper()


class OrgMemberForm(forms.ModelForm):
    class Meta:
        model = OrgMember
        fields = ["name", "position", "photo", "parent", "level", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["parent"].queryset = self.fields["parent"].queryset.exclude(pk=self.instance.pk)
        self.helper = dashboard_helper()


class FounderForm(forms.ModelForm):
    class Meta:
        model = Founder
        fields = ["name", "position", "photo", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = ["name", "logo", "type", "description", "website_url", "order"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "category", "file", "published_date"]
        widgets = {"published_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.filter(context="document")
        self.helper = dashboard_helper()
