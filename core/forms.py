from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, SetPasswordForm
from django.core.exceptions import ValidationError
from django.db import transaction
from django_quill.forms import QuillFormField
from django_quill.widgets import QuillWidget

from core.models import Publication, Project, Photo, User, InvitationCode, Award, GPUStatus, AdminToken, Post, \
    PasswordResetToken


class SignupForm(UserCreationForm):
    invitation_code = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile_image"].required = True

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "profile_image", "position_start_date", "website", "birthday",
                  "phone_number", "secondary_email", "research_topics"]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Yoshua",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Bengio",
            }),
            "position_start_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "birthday": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "research_topics": forms.TextInput(),
        }

    def clean_invitation_code(self):
        data = self.cleaned_data["invitation_code"]
        invitation_code: InvitationCode = InvitationCode.objects.filter(code=data).first()
        if not invitation_code:
            raise ValidationError("Invalid invitation code")
        if invitation_code.uses_remaining <= 0:
            raise ValidationError("Invitation code is expired")
        self.invitation_code = invitation_code
        return data

    def clean_email(self):
        data = self.cleaned_data["email"]
        existing_user = User.objects.filter(email=data).first()
        if existing_user:
            raise ValidationError("Email is already in use")
        return data


class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["position"].disabled = True

    class Meta:
        model = User
        fields = ["position", "profile_image", "first_name", "last_name", "email", "position_start_date",
                  "position_end_date", "website", "github", "scholar", "twitter", "birthday", "phone_number",
                  "secondary_email", "research_topics", "current_position"]
        widgets = {
            "first_name": forms.TextInput(attrs={
                "placeholder": "Yoshua",
            }),
            "last_name": forms.TextInput(attrs={
                "placeholder": "Bengio",
            }),
            "position_start_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "position_end_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "birthday": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "research_topics": forms.TextInput(),
        }


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ["type", "title", "published_date", "authors", "venue", "image", "tags", "pdf_link", "code_link",
                  "video_link"]
        help_texts = {
            "tags": "Hold down ctrl, or cmd on a Mac, to select more than one."
        }
        widgets = {
            "published_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "title": forms.TextInput(),
            "authors": forms.TextInput(),
            "venue": forms.TextInput(),
        }


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "organization", "members", "image", "summary", "start_date", "end_date"]
        widgets = {
            "title": forms.TextInput(),
            "organization": forms.TextInput(),
            "members": forms.TextInput(),
            "start_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "end_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
        }


class AwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ["name", "awardees", "awarded_date", "venue", "paper", "image", "pdf_link", "code_link", "video_link"]
        widgets = {
            "awardees": forms.TextInput(),
            "awarded_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "venue": forms.TextInput(),
            "paper": forms.TextInput(),
        }


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "description", "taken_date"]
        widgets = {
            "taken_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
        }


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["published_date", "title", "body"]
        widgets = {
            "title": forms.TextInput(),
        }


class PhotoFormWithoutImage(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["description", "taken_date"]
        widgets = {
            "taken_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
        }


class PasswordResetForm(forms.Form):
    error_messages = {
        'invalid_token': "Incorrect email or token",
        'invalid_email': "Invalid email",
    }
    email = forms.EmailField()
    password_reset_token = forms.CharField(label="Password reset token", max_length=40)
    new_password = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    def clean_new_password(self):
        password = self.cleaned_data.get('new_password')
        password_validation.validate_password(password)
        return password

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise ValidationError(self.error_messages["invalid_email"], code="invalid_email")
        return email

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        token = cleaned_data.get("password_reset_token")
        email = cleaned_data.get("email")
        if email and new_password:
            token_object = PasswordResetToken.objects.filter(user__email=email, token=token).first()
            if token_object is None:
                raise ValidationError(self.error_messages["invalid_token"], code="invalid_token")
            self.token = token_object
        return cleaned_data

    def save(self, commit=True):
        password = self.cleaned_data["new_password"]
        user = self.token.user
        token = self.token
        with transaction.atomic():
            user.set_password(password)
            token.delete()
            if commit:
                token.user.save()
        return user


class GPUStatusForm(forms.ModelForm):
    admin_token = forms.CharField(max_length=40)

    class Meta:
        model = GPUStatus
        fields = ["server_name", "status"]
        widgets = {
            "server_name": forms.TextInput(attrs={
                "placeholder": "osi1",
            }),
        }

    def clean_admin_token(self):
        token = self.cleaned_data["admin_token"]
        if not AdminToken.objects.filter(token=token).first():
            raise ValidationError("Invalid admin token")
        return token


class AdminPublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ["type", "title", "published_date", "authors", "venue", "image", "tags", "pdf_link", "code_link",
                  "video_link", "public"]
        help_texts = {
            "tags": "Hold down ctrl, or cmd on a Mac, to select more than one."
        }
        widgets = {
            "published_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "title": forms.TextInput(),
            "authors": forms.TextInput(),
            "venue": forms.TextInput(),
        }


class AdminProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "organization", "members", "image", "summary", "start_date", "end_date", "priority",
                  "public"]
        widgets = {
            "title": forms.TextInput(),
            "organization": forms.TextInput(),
            "members": forms.TextInput(),
            "start_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "end_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
        }


class AdminAwardForm(forms.ModelForm):
    class Meta:
        model = Award
        fields = ["name", "awardees", "awarded_date", "venue", "paper", "image", "pdf_link", "code_link", "video_link",
                  "public"]
        widgets = {
            "awardees": forms.TextInput(),
            "awarded_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
            "venue": forms.TextInput(),
            "paper": forms.TextInput(),
        }


class AdminPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "description", "taken_date", "starred", "public"]
        widgets = {
            "taken_date": forms.TextInput(attrs={
                "placeholder": "YYYY-MM-DD",
            }),
        }
