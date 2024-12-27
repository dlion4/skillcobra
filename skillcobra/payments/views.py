import json
import random
import string
import time
from decimal import Decimal

import requests
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from skillcobra.payments.forms import CoursePurchasePaymentForm
from skillcobra.payments.models import Transaction
from skillcobra.payments.tasks import create_student_success_payment_transaction
from skillcobra.school.models import Course

from .utils import handle_payment_processing_view


# Create your views here.
class ProcessPaymentFormView(View):
    form_class = CoursePurchasePaymentForm

    @method_decorator(login_required, csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile = request.user.user_profile
        form = self.form_class(request.POST, profile=profile)
        if form.is_valid():
            return self.handle_payment_method(form)
        return JsonResponse(
            {"detail": "Form field errors. Please verify the detail to proceed"},
            status=200,
        )

    def handle_payment_method(self, form):
        data = form.cleaned_data
        profile = self.request.user.user_profile
        if data.get("coupon") == "Jeckon":
            data["amount"] = data["amount"] * Decimal("0.9")  # Apply coupon discount
        response = handle_payment_processing_view(data, profile)
        if response.get("status") == "success":
            money_data = response.get("amount")
            for pk in json.loads(data.get("courses_ids", None)):
                course = Course.objects.get(pk=int(pk))
                course.sales_count += 1
                course.save()
                payment_details = {
                    "amount": str(money_data),
                    "currency": "USD",
                    "account_type": response.get("accountType", "CARD"),
                    "payment_reference": str(
                        str(response.get("referenceId")) + f"_{time.time()}"),
                }
                self._create_payment_success_transaction(
                    student=profile,
                    parent=course,
                    payment_details=payment_details,
                )
        return JsonResponse(
            {"detail": "success_message", "url": reverse("students:dashboard")},
            status=200,
        )

    def _create_payment_success_transaction(self, student, parent, payment_details):
        from skillcobra.payments.threads import DatabaseInsertionThreadPool
        thread_pool = DatabaseInsertionThreadPool()
        thread_pool.submit(
            create_student_success_payment_transaction,
            student=student,
            parent=parent,
            payment_details=payment_details,
        )


class CheckPaymentStatusView(View):
    @method_decorator(login_required, csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, student_pk):
        try:
            status_record = Transaction.objects.get(student_id=student_pk)
            return JsonResponse(
                {
                    "status": "Success",
                    "message": f"Payment for {status_record.parent} processed successfully",
                },
            )
        except Transaction.DoesNotExist:
            return JsonResponse(
                {
                    "status": "Pending",
                    "message": "Your payment is still being processed.",
                },
            )
