from time import sleep
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView

from skillcobra.users.models import Profile

from .forms import UpdateAccountProfileBasicDataForm
from .forms import UserLoginForm
from .forms import UserRegistrationForm


class LoginView(FormView):
    template_name = "account/login.html"
    form_class = UserLoginForm
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None and user.is_active:
                login(request, user)
                return JsonResponse({"url": str(reverse("home"))}, status=200)
            return JsonResponse(
                {"detail": "No user with the provided credentials"}, status=404)
        return JsonResponse({"detail": "Invalid request or server"}, status=500)


class RegisterView(FormView):
    form_class = UserRegistrationForm
    template_name = "account/register.html"
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            try:
                form.save()
                return JsonResponse({"url": str(reverse("users:login"))}, status=201)
            except Exception as e:  # noqa: BLE001
                return JsonResponse({"detail": str(e)},status=500)
        return JsonResponse({"detail": form.errors.as_json()}, status=400)

class RequestPasswordResetView(TemplateView):
    template_name = "account/request_password_reset.html"
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse("home"))
        return super().dispatch(request, *args, **kwargs)
class LogoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({"url": reverse("users:login")})


class UpdateProfileView(View):
    account_basic_form = UpdateAccountProfileBasicDataForm

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile = request.user.user_profile
        form = self.account_basic_form(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return JsonResponse({}, status=200)
        return JsonResponse({"detail": form.errors.as_json()}, status=400)
