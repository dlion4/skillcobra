import random
import string
import time
from datetime import timedelta

import requests
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import DetailView
from django.views.generic import TemplateView

from skillcobra.memberships.models import MemberShip
from skillcobra.memberships.models import MemberShipPayment
from skillcobra.memberships.models import Plan
from skillcobra.memberships.models import Question
from skillcobra.payments.forms import BillingAddressForm
from skillcobra.payments.forms import CreditDebitMembershipPaymentForm
from skillcobra.payments.tasks import (
    create_membership_purchase_success_payment_transaction,
)


class MembershipView(TemplateView):
    template_name = "membership/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["student_plan"] = Plan.objects.filter(name="S").first()
        context["instructor_plan"] = Plan.objects.filter(name="I").first()
        context["plan_questions"] = self.get_plan_questions()
        return context

    def get_plan_questions(self):
        plan_content_type = ContentType.objects.get_for_model(Plan)
        return (
            ContentType.objects.get_for_model(Question)
            .model_class()
            .objects.filter(content_type=plan_content_type)
            .filter(question__isnull=False)
            .order_by("-timestamp")
        )


class MembershipPaymentView(LoginRequiredMixin, DetailView):
    template_name = "membership/payment.html"
    model = Plan
    context_object_name = "plan"
    billing_address_form = BillingAddressForm
    debit_credit_form = CreditDebitMembershipPaymentForm

    def get_object(self, queryset=...):
        name = self.kwargs.get("name")
        return get_object_or_404(
            self.model,
            pk=self.kwargs.get("pk"),
            name=name.upper(),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["billing_address_form"] = self.billing_address_form(
            profile=self.request.user.user_profile,
        )
        context["debit_credit_form"] = self.debit_credit_form(
            profile=self.request.user.user_profile,
        )
        return context

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        profile = request.user.user_profile
        post_data = request.POST.copy()
        price = post_data.pop("order_price")
        if isinstance(price, list) and price:
            price = {"price": price[0]}
        form = self.debit_credit_form(post_data, profile=profile)
        if form.is_valid():
            data = form.cleaned_data
            data.update(price)
            payment_upload_data = self._prepare_data_to_payment_details(profile, data)
            response = requests.post(
                str(settings.SYNCPAY_MERCHANT_PAYMENT_URL),
                json=payment_upload_data,
                timeout=10,
            )
            response.raise_for_status()
            res = response.json()
            transaction_response = res.get("createTransactionResponse").get(
                "transactionResponse",
            )
            if (
                res.get("createTransactionResponse").get("messages").get("resultCode")
                == "Error"
            ):
                error_message = (
                    transaction_response.get("errors").get("error").get("errorText")
                )
                return JsonResponse({"detail": error_message}, status=400)
            return self._handle_membership_payment_and_creation(
                transaction_response,
                res,
                profile,
            )
        return JsonResponse(
            {"detail": "Error submitting your form. Check and retry"},
            status=400,
            safe=False,
        )

    def _handle_membership_payment_and_creation(
        self,
        transaction_response,
        res,
        profile,
    ):
        money_data = res.get("createTransactionResponse").get("amount")
        plan = self.get_object(self.model)
        membership, _ = MemberShip.objects.get_or_create(
            profile=profile,
            plan=plan,
            defaults={"end_date": timezone.now() + timedelta(days=30)},
        )
        membership_payment = MemberShipPayment.objects.create(
            user=profile,
            amount=str(money_data.get("value")),
            payment_method=str(transaction_response.get("accountType")),
            subscription=membership,
        )
        membership.renew()
        payment_details = {
            "amount": str(membership_payment.amount),
            "currency": str(money_data.get("currency")),
            "account_type": str(membership_payment.payment_method),
            "payment_reference": str(
                str(
                    res.get("createTransactionResponse").get("refId"),
                )
                + f"_{time.time()}",
            ),
        }
        self._create_payment_success_transaction(profile, payment_details)
        return JsonResponse(payment_details, status=200, safe=False)

    def _create_payment_success_transaction(self, parent, payment_details):
        from skillcobra.payments.threads import DatabaseInsertionThreadPool

        thread_pool = DatabaseInsertionThreadPool()
        thread_pool.submit(
            create_membership_purchase_success_payment_transaction,
            parent=parent,
            payment_details=payment_details,
        )

    def _prepare_data_to_payment_details(self, profile, data):
        return {
            "cardNumber": data.get("card_number"),
            "expirationDate": "2035-02",
            "cardCode": data.get("card_cvv_number"),
            "invoiceNumber": "".join(
                random.choices(  # noqa: S311
                    population=string.ascii_uppercase,
                    k=11,
                ),
            ),
            "description": "Membership Purchase",
            "itemId": "22",
            "itemDescription": f"Membership Purchase of <{self.get_object().get_name_display()}> by {profile.full_name()}",  # noqa: E501
            "itemTotalPrice": str(data.get("price")),
            "customer_email": str(profile.user.email),
        }
