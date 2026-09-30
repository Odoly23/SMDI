from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from .models import ContactMessage


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
