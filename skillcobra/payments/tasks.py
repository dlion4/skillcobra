import contextlib
from datetime import datetime
from decimal import Decimal

from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db import transaction

from roles.instructors.instructor.models import Account
from roles.instructors.instructor.models import CourseSale
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
    transaction_ = Transaction.objects.create(
        student=student,
        content_type=ContentType.objects.get_for_model(parent),
        object_id=parent.id,
        status=TransactionStatus.SUCCESS,
        payment_intent=TransactionIntentChoices.CP,
        amount=payment_details.get("amount"),
        currency=payment_details.get("currency", "USD"),
        payment_method=payment_details.get("payment_method", "CARD"),
        payment_reference=payment_details.get("payment_reference"),
        account_type=payment_details.get("account_type"),
    )
    sales, _ = CourseSale.objects.get_or_create(
        tutor=transaction_.parent.tutor,
    )
    if transaction_.pk not in sales.transactions.values_list(
        "pk", flat=True,
    ) and parent.pk not in sales.courses.values_list("pk", flat=True):
        sales.transactions.add(transaction_)
        sales.courses.add(parent)
        sales.save()
    with contextlib.suppress(Cart.DoesNotExist):
        student_cart = Cart.objects.get(student=student)
        if parent.pk in student_cart.courses.values_list("pk", flat=True):
            student_cart.courses.remove(parent)
            student.save()
            bank_account, _ = Account.objects.get_or_create(holder=parent.tutor)
            bank_account.account_balance += float(transaction_.amount)
            bank_account.save()
        if  parent.pk not in student.purchased_courses.values_list("pk", flat=True):
            student.purchased_courses.add(parent)
            student.save()
