from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView


class TemplateViewMixin(TemplateView):
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
