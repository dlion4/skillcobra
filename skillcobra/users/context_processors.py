from django.conf import settings

from .forms import UpdateAccountProfileBasicDataForm


def allauth_settings(request):
    """Expose some settings from django-allauth in templates."""
    return {
        "ACCOUNT_ALLOW_REGISTRATION": settings.ACCOUNT_ALLOW_REGISTRATION,
    }


def account_related_settings(request):
    form = UpdateAccountProfileBasicDataForm
    if request.user.is_authenticated:
        profile = request.user.user_profile
    return {"account_basic_update_form": form(instance=profile)}
