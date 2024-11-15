from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from skillcobra.payments.choices import TransactionIntentChoices
from skillcobra.payments.choices import TransactionStatus
from skillcobra.payments.utils import generate_reference_id


class Plan(models.Model):
    name = models.CharField(
        max_length=1,
        unique=True,
        choices=(("B", "Basic"), ("P", "Pro")),
        default="B",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.50)
    duration = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.get_name_display()} Plan"


class PlanFeature(models.Model):
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="plan_features"
    )
    feature = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.plan.get_name_display()} Plan Feature"


# Create your models here.
class MemberShip(models.Model):
    profile = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="profile_membership"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="membership_plan"
    )
    status = models.CharField(
        max_length=1,
        choices=(
            ("A", "Active"),
            ("I", "Inactive"),
            ("C", "Cancelled"),
            ("P", "Paused"),
        ),
        default="I",
    )
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.profile.user.username} - {self.plan.get_name_display()} Plan"


class Transaction(models.Model):
    student = models.ForeignKey(
        "users.Profile", on_delete=models.CASCADE, related_name="student_transactions",
    )
    content_type = models.ForeignKey(
        ContentType, on_delete=models.SET_NULL, null=True, blank=True,
    )
    object_id = models.PositiveIntegerField(null=True, blank=True)
    parent = GenericForeignKey("content_type", "object_id")
    status = models.CharField(
        _("Status"),
        max_length=30,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PENDING,
    )
    amount = models.DecimalField(max_digits=16, decimal_places=2, default=0.00)
    timestamp = models.DateTimeField(auto_now_add=True)
    payment_intent = models.CharField(
        max_length=300,
        choices=TransactionIntentChoices.choices,
        default=TransactionIntentChoices.CP)
    currency = models.CharField(max_length=30,default="USD")
    payment_method = models.CharField(max_length=30, default="CARD")
    reference = models.CharField(max_length=46, blank=True)
    account_type = models.CharField(max_length=100, blank=True)
    payment_reference = models.CharField(max_length=300, blank=True)
    class Meta:
        ordering = ("-timestamp",)
    def __str__(self):
        return f"{self.student.full_name} - {self.status} - {self.amount}"
    def save(self, *args, **kwargs):
        instance = super().save(*args, **kwargs)
        self.reference = generate_reference_id(instance)
        return instance
