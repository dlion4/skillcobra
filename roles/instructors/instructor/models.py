from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.db import models

from roles.instructors.instructor.choices import AccountIntentChoice
from skillcobra.payments.models import Transaction
from skillcobra.school.models import Course

# Create your models here.


def validate_intent_reason(value):
    """
    Custom validation for intent_reason based on the intent field.
    """
    if not hasattr(value, "instance"):
        return
    account = value.instance
    if not value.strip() and account.intent in [
        AccountIntentChoice.R,
        AccountIntentChoice.P,
    ]:
        msg = f"Intent Reason is required for this {account.intent} intent."
        raise ValidationError(msg)

def validate_tutor_role(value):
    course_sale = value.instance
    if not hasattr(value, "instance"):
        return
    if course_sale.user.role != "instructor":
        msg = "This instance must be a tutor to proceed!"
        raise ValidationError(msg)

class CourseSale(models.Model):
    tutor = models.OneToOneField(
        "users.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tutor_sales",
        validators=[validate_tutor_role],
    )
    transactions = models.ManyToManyField(
        Transaction,
        related_name="course_sales",
        blank=True,
    )
    courses = models.ManyToManyField(
        Course,
        related_name="sales_course",
        blank=True,
    )
    timestamp = models.DateTimeField(auto_now_add=True)
    modified_timestamp = models.DateTimeField(auto_now=True)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"Course Sale: {self.course.title} - Tutor: {self.tutor.user.username}"


class Account(models.Model):
    holder = models.OneToOneField(
        "users.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile_bank_account",
    )
    intent = models.CharField(
        max_length=10,
        choices=AccountIntentChoice.choices,
        default=AccountIntentChoice.D,
    )
    intent_reason = models.CharField(
        max_length=300,
        blank=True,
        validators=[validate_intent_reason],
    )
    account_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Bank Account for {self.holder.full_name()}"
