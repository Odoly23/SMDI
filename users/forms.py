from django import forms
from django.contrib.auth.models import User, Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from main.crispy import dashboard_helper
from users.models import GROUP_ADMIN, GROUP_STAFF, GROUP_MEMBER

GROUP_CHOICES = [(GROUP_ADMIN, "Admin"), (GROUP_STAFF, "Staff"), (GROUP_MEMBER, "Member")]


class StaffUserCreateForm(forms.Form):
    """Kria User foun + Profile + Group hamutuk iha formuláriu ida deit."""
    username = forms.CharField(max_length=150, label="Username")
    first_name = forms.CharField(max_length=150, label="Naran Boot")
    last_name = forms.CharField(max_length=150, required=False, label="Apelidu")
    email = forms.EmailField(required=False, label="Email")
    group = forms.ChoiceField(choices=GROUP_CHOICES, label="Grupu/Rola")
    position = forms.CharField(max_length=150, required=False, label="Kargu/Jabatan")
    phone = forms.CharField(max_length=30, required=False, label="Telefone")
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False, label="Bio")
    photo = forms.ImageField(required=False, label="Foto")
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Konfirma Password")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = dashboard_helper()

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username ne'e uza ona.")
        return username

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 and p2 and p1 != p2:
            raise ValidationError("Password sira la hanesan.")
        if p1:
            validate_password(p1)
        return cleaned

    def save(self):
        data = self.cleaned_data
        user = User.objects.create_user(
            username=data["username"], email=data.get("email", ""),
            first_name=data["first_name"], last_name=data.get("last_name", ""),
            password=data["password1"],
        )
        group, _ = Group.objects.get_or_create(name=data["group"])
        user.groups.set([group])
        profile = user.profile
        profile.position = data.get("position", "")
        profile.phone = data.get("phone", "")
        profile.bio = data.get("bio", "")
        if data.get("photo"):
            profile.photo = data["photo"]
        profile.save()
        return user


class StaffUserUpdateForm(forms.Form):
    """Edita User + Profile + Group. Password mamuk = la troka password."""
    first_name = forms.CharField(max_length=150, label="Naran Boot")
    last_name = forms.CharField(max_length=150, required=False, label="Apelidu")
    email = forms.EmailField(required=False, label="Email")
    group = forms.ChoiceField(choices=GROUP_CHOICES, label="Grupu/Rola")
    is_active = forms.BooleanField(required=False, label="Ativu", initial=True)
    position = forms.CharField(max_length=150, required=False, label="Kargu/Jabatan")
    phone = forms.CharField(max_length=30, required=False, label="Telefone")
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False, label="Bio")
    photo = forms.ImageField(required=False, label="Foto")
    password1 = forms.CharField(
        widget=forms.PasswordInput, required=False, label="Password Foun (mamuk se la troka)"
    )
    password2 = forms.CharField(widget=forms.PasswordInput, required=False, label="Konfirma Password Foun")

    def __init__(self, *args, instance=None, **kwargs):
        self.instance = instance
        initial = kwargs.pop("initial", {}) or {}
        if instance is not None:
            initial.setdefault("first_name", instance.first_name)
            initial.setdefault("last_name", instance.last_name)
            initial.setdefault("email", instance.email)
            initial.setdefault("is_active", instance.is_active)
            initial.setdefault(
                "group", instance.groups.first().name if instance.groups.exists() else GROUP_MEMBER
            )
            if hasattr(instance, "profile"):
                initial.setdefault("position", instance.profile.position)
                initial.setdefault("phone", instance.profile.phone)
                initial.setdefault("bio", instance.profile.bio)
        super().__init__(*args, initial=initial, **kwargs)
        self.helper = dashboard_helper()

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get("password1"), cleaned.get("password2")
        if p1 or p2:
            if p1 != p2:
                raise ValidationError("Password sira la hanesan.")
            validate_password(p1)
        return cleaned

    def save(self):
        data = self.cleaned_data
        user = self.instance
        user.first_name = data["first_name"]
        user.last_name = data.get("last_name", "")
        user.email = data.get("email", "")
        user.is_active = data.get("is_active", True)
        if data.get("password1"):
            user.set_password(data["password1"])
        user.save()
        group, _ = Group.objects.get_or_create(name=data["group"])
        user.groups.set([group])
        profile = user.profile
        profile.position = data.get("position", "")
        profile.phone = data.get("phone", "")
        profile.bio = data.get("bio", "")
        if data.get("photo"):
            profile.photo = data["photo"]
        profile.save()
        return user
