import contextlib
from time import sleep
from django.db import transaction
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import FormView
from django.views.generic import TemplateView

from skillcobra.payments.forms import BillingAddressForm
from skillcobra.payments.forms import PayoutAccountForm
from skillcobra.payments.models import BillingAddress
from skillcobra.payments.models import PayoutAccount
from skillcobra.users.models import Profile, User

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
            user = User.objects.all()
            print(user)
            user = authenticate(
                request,
                username=form.cleaned_data.get("email"),
                password=form.cleaned_data.get("password"),
            )
            if user is not None and user.is_active:
                login(request, user)
                return JsonResponse({"url": str(reverse("home"))}, status=200)
            return JsonResponse(
                {"detail": "No user with the provided credentials"}, status=404,
            )
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
                return JsonResponse({"detail": str(e)}, status=500)
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


class UpdateProfileAddressView(View):
    form = BillingAddressForm

    @method_decorator(login_required, csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile = request.user.user_profile
        form = self.form(request.POST, profile=profile)
        if form.is_valid():
            try:
                billing_address = BillingAddress.objects.get(
                    owner=profile,
                )
                for field, value in form.cleaned_data.items():
                    setattr(billing_address, field, value)
                billing_address.save()
            except BillingAddress.DoesNotExist:
                billing_address = form.save(commit=False)
                billing_address.owner = profile
                billing_address.save()
            return JsonResponse(
                {
                    "success": True,
                    "message": "Address saved successfully",
                    "address_id": str(profile.profile_billing_address.pk),
                },
                status=200,
            )

        return JsonResponse(
            {"error": "Something went wrong and could not save your address"},
            status=400,
        )


class CreatePayoutAccountView(View):
    form_class = PayoutAccountForm

    def post(self, request:HttpRequest, *args, **kwargs):
        post_data = request.POST.copy()
        address_id = post_data.pop("address_id")
        form = self.form_class(post_data)
        if form.is_valid():
            data = form.cleaned_data
            account_type = data.get("account_type")
            extra_data = {
                "account_number": data.get("account_number"),
                "account_name": data.get("account_name"),
                "bank_name": data.get("bank_name"),
                "email_address": data.get("email_address"),
                "phone_number": data.get("phone_number"),
            }
            with transaction.atomic():
                payout_account = PayoutAccount(
                    owner=request.user.user_profile,
                    account_type=account_type,
                    address_id=address_id[0],
                )
                payout_account.save(extra_data=extra_data)
                return JsonResponse(
                    {"success": True, "message": "Payout account created successfully."},
                    status=200,
                )
        return JsonResponse({"detail": "Something went terribly wrong"}, status=400)
