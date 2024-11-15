import contextlib
from datetime import datetime

from django.db import models
from django.db import transaction

from skillcobra.payments.choices import TransactionIntentChoices
from skillcobra.payments.choices import TransactionStatus
from skillcobra.payments.models import Transaction
from skillcobra.purchases.models import Cart
from skillcobra.users.models import Profile


@transaction.atomic
def create_student_success_payment_transaction(
    student: type[Profile],
    parent: type[models.Model],
    payment_details: dict,
):
    """
    CP: course purchase
    """
    # transaction = Transaction.objects.create(
    #     student=student,
    #     parent=parent,
    #     status=TransactionStatus.SUCCESS,
    #     payment_intent=TransactionIntentChoices.CP,
    #     amount=payment_details.get("amount"),
    #     currency=payment_details.get("currency", "USD"),
    #     payment_method=payment_details.get("payment_method", "CARD"),
    #     payment_reference=payment_details.get("payment_reference"),
    #     account_type=payment_details.get("account_type"),
    # )
    print(payment_details)
    # with contextlib.suppress(Cart.DoesNotExist):
    #     student_cart = Cart.objects.get(student=student)
    #     if parent.pk in student_cart.courses.values_list("pk", flat=True):
            # student_cart.courses.remove(parent)
            # student.save()
        #     print("course item found in stduent cart ", parent)
        # print("student cart ", student_cart)
    print("Preparing creating transaction fro  the student")
