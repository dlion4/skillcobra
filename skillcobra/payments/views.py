import json
import random
import string
from decimal import Decimal

import requests
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from skillcobra.payments.forms import CoursePurchasePaymentForm
from skillcobra.payments.tasks import create_student_success_payment_transaction
from skillcobra.payments.threads import DatabaseInsertionThreadPool
from skillcobra.school.models import Course


thread_pool = DatabaseInsertionThreadPool()

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
        payment_upload_data = {
            "cardNumber": data.get("card_number"),
            "expirationDate": "2035-02",
            "cardCode": data.get("cvv"),
            "invoiceNumber": "".join(
                random.choices(  # noqa: S311
                    population=string.ascii_uppercase,
                    k=11,
                ),
            ),
            "description": "course purchase",
            "itemId": "22",
            "itemDescription": "This is purchase for course",
            "itemTotalPrice": str(data.get("amount")),
        }
        response = requests.post(
            "http://localhost:8001",
            json=payment_upload_data,
            timeout=10,
        )
        response.raise_for_status()
        res = response.json()
        print(res)
        if (
            res.get("createTransactionResponse").get("messages").get("resultCode")
            == "Error"
        ):
            error_message = (
                res.get("createTransactionResponse")
                .get("transactionResponse")
                .get("errors")
                .get("error")
                .get("errorText")
            )
            return JsonResponse({"detail": error_message}, status=400)
        if (
            res.get("createTransactionResponse").get("messages").get("resultCode")
            == "Ok"
        ):
            success_message = (
                res.get("createTransactionResponse")
                .get("transactionResponse")
                .get("messages")
                .get("message")
                .get("description")
            )
            for pk in json.loads(data.get("courses_ids", None)):
                course = Course.objects.get(pk=int(pk))
                self._create_payment_success_transaction(
                    student=profile,
                    parent=course,
                    payment_details={
                        "amount": str(
                            res.get("createTransactionResponse")
                            .get("amount")
                            .get("value"),
                        ),
                        "currency": str(
                            res.get("createTransactionResponse")
                            .get("amount")
                            .get("currency"),
                        ),
                    },
                )
            return JsonResponse({"detail": success_message}, status=200)
        return JsonResponse({"response": "Payment processed successfully"})
    def _create_payment_success_transaction(self, student, parent, payment_details):
        thread_pool.submit(
            create_student_success_payment_transaction,
            student=student,
            parent=parent,
            payment_details=payment_details,
        )
