import secrets
import string
from decimal import Decimal

from django.db import models
from django.utils.timezone import timedelta

from skillcobra.payments.models import PayoutAccount
from skillcobra.users.models import Profile


class InstructorPayout(models.Model):
    instructor = models.ForeignKey(
        Profile,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profile_instructor_payouts",
    )
    channel = models.ForeignKey(
        PayoutAccount,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="profile_payout_channels",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    fee = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    paid = models.DecimalField(max_digits=12, decimal_places=2, default="0.00")
    initiated_timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=(
            ("initiated", "Initiated"),
            ("completed", "Completed"),
            ("cancelled", "Cancelled"),
            ("failed", "Failed"),
        ),
        default="initiated",
    )
    reference_stamp = models.CharField(max_length=19, blank=True)

    def __str__(self):
        return f"Payout status: ({self.status!s})"

    def save(self, *args, **kwargs):
        if not self.reference_stamp:
            self.reference_stamp = self._generate_reference_stamp()
        self._calculate_fee()
        super().save(*args, **kwargs)

    def next_payout_status(self):
        return timedelta(days=28) + self.initiated_timestamp

    def _generate_reference_stamp(self):
        return "".join(
            secrets.choice(string.ascii_uppercase + string.digits + str(self.pk))
            for _ in range(12)
        )
    def _calculate_fee(self):
        self.paid = self.amount * Decimal("0.87")
        self.fee = self.amount - self.paid
