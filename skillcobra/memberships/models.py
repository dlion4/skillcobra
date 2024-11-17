from datetime import timedelta

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Plan(models.Model):
    name = models.CharField(
        max_length=1,
        unique=True,
        choices=(("S", "Student"), ("I", "Instructor")),
        default="S",
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.50)
    duration = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.get_name_display()} Plan"

    def get_absolute_url(self):
        return reverse(
            "payments:shared:membership_payment_view",
            kwargs={"pk": self.pk, "name": self.name.lower()},
        )


class PlanFeature(models.Model):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="plan_features",
    )
    feature = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_available = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["plan", "feature"], name="unique_plan_feature"
            ),
        ]

    def __str__(self):
        return f"{self.plan.get_name_display()} Plan Feature"


# Create your models here.
class MemberShip(models.Model):
    profile = models.OneToOneField(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="profile_membership",
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.CASCADE,
        related_name="membership_plan",
    )
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    status = models.CharField(
        max_length=1,
        choices=(
            ("A", "Active"),
            ("C", "Cancelled"),
            ("P", "Paused"),
        ),
        default="A",
    )

    def __str__(self):
        return f"{self.profile.full_name()}'s Subscription"

    def is_expired(self):
        return timezone.now() > self.end_date

    def renew(self):
        """Renew the subscription for another month."""
        self.end_date = timezone.now() + timedelta(days=30)
        self.save()

    def cancel(self):
        """Cancel subscription, setting the end date to today."""
        self.end_date = timezone.now()
        self.is_active = False
        self.save()

    def get_subscription_duration(self):
        """Get the number of days until subscription expires."""
        return (self.end_date - timezone.now()).days


class MemberShipPayment(models.Model):
    user = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="payments",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=50.00)
    date_paid = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    subscription = models.ForeignKey(
        MemberShip,
        on_delete=models.CASCADE,
        related_name="membership_payments",
    )

    def __str__(self):
        return (
            f"Payment of {self.amount} by {self.user.full_name()} on {self.date_paid}"
        )


class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class FeatureAccess(models.Model):
    user = models.ForeignKey("users.Profile", on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    subscription = models.ForeignKey(MemberShipPayment, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} access to {self.feature.name}"


class Question(models.Model):
    """Model definition for Question."""

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    parent = GenericForeignKey("content_type", "object_id")
    question = models.CharField(max_length=255)
    answer = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        """Meta definition for Question."""

        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        """Unicode representation of Question."""
        return f"{self.question} <{self.parent.__class__.__name__.lower()}>"


class MembershipCardCapture(models.Model):
    """Model definition for CardCapture"""

    profile = models.ForeignKey(
        "users.Profile",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="profile_card_capture",
    )
    card_number = models.CharField(max_length=24)
    card_holder_name = models.CharField(max_length=100)
    card_cvv_number = models.CharField(max_length=200)
    expiry_month = models.CharField(
        max_length=2,
        choices=tuple(
            zip(
                range(1, 13),
                [
                    "January",
                    "February",
                    "March",
                    "April",
                    "May",
                    "June",
                    "July",
                    "August",
                    "September",
                    "October",
                    "November",
                    "December",
                ],
                strict=False,
            ),
        ),
    )
    expiry_year = models.CharField(
        max_length=4,
    )

    def __str__(self):
        """Unicode representation of CardCapture"""
        return str(self.card_holder_name)
