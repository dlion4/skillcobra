from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """

class UserRegistrationForm(forms.ModelForm):
    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(
            attrs={"class": "prompt srch_explore", "placeholder": "Email Address"}),
    )
    role = forms.CharField(widget=forms.HiddenInput())
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "prompt srch_explore", "placeholder": "Password"}),
    )
    password2 = forms.CharField(
        label=_("Confirm Password"),
        widget=forms.PasswordInput(
            attrs={"class": "prompt srch_explore", "placeholder": "Confirm Password"}
        ),
    )
    PASSWORD_MIN_LENGTH=8
    class Meta:
        model = User
        fields = ("email","password1","password2")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")

        # Validate that the passwords match and are at least 8 characters long
        if password1 != password2:
            raise forms.ValidationError(_("Passwords must match."))

        if len(password1) < self.PASSWORD_MIN_LENGTH:
            raise forms.ValidationError(
                _("Passwords must be at least 8 characters long.")
            )

        return cleaned_data

    def save(self, commit=True):  # noqa: FBT002
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])  # Set the hashed password
        user.role = self.cleaned_data.get("role")
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    email = forms.EmailField(
        label=_("Email Address"),
        widget=forms.EmailInput(
            attrs={"class": "prompt srch_explore", "placeholder": "Email Address"}),
    )
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(
            attrs={"class": "prompt srch_explore", "placeholder": "Password"}),
    )
