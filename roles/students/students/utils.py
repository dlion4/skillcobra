from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from skillcobra.users.models import Profile


class TemplateViewMixin(LoginRequiredMixin, TemplateView):
    template_name = ""

    def get_template_names(self):
        return [f"students/{self.template_name}"]

    def dispatch(self, request, *args, **kwargs):
        if (
            request.user.is_authenticated
            and request.user.role in ["student"]
            and not any(
                request.path.startswith(path) for path in ["/student"]
            )
        ):
            return redirect(reverse(f"{request.user.role.lower()}s:dashboard"))
        return super().dispatch(request, *args, **kwargs)

    def get_profile(self)->Profile:
        return self.request.user.user_profile

    def get_dashboard_url(self):
        return str(reverse("students:dashboard"))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile"] = self.get_profile()
        context["dashboard_url"] = self.get_dashboard_url()
        return context
