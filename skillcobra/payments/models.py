from datetime import timedelta

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from skillcobra.payments.choices import PayoutAccountChoices
from skillcobra.payments.choices import TransactionIntentChoices
from skillcobra.payments.choices import TransactionStatus
from skillcobra.payments.utils import generate_reference_id


class Transaction(models.Model):
    student = models.ForeignKey(
        "users.Profile",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="student_transactions",
    )
    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
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
        default=TransactionIntentChoices.CP,
    )
    currency = models.CharField(max_length=30, default="USD")
    payment_method = models.CharField(max_length=30, default="CARD")
    reference = models.CharField(max_length=46, blank=True)
    account_type = models.CharField(max_length=100, blank=True)
    payment_reference = models.CharField(max_length=300, blank=True)

    class Meta:
        ordering = ("-timestamp",)

    def __str__(self):
        return f"{self.student.full_name} - {self.status} - {self.amount}"

    def save(self, *args, **kwargs):
        self.reference = generate_reference_id()
        super().save(*args, **kwargs)


class BillingAddress(models.Model):
    owner = models.OneToOneField(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="profile_billing_address",
    )
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    country = CountryField()
    address_line1 = models.CharField(max_length=255, blank=True)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.owner.full_name} - {self.country} - {self.address_line1}"


class PayoutAccount(models.Model):
    owner = models.ForeignKey(
        "users.Profile",
        on_delete=models.CASCADE,
        related_name="payout_accounts",
    )
    address = models.ForeignKey(
        BillingAddress, on_delete=models.SET_NULL, blank=True, null=True,
    )
    account_type = models.CharField(
        max_length=10,
        choices=PayoutAccountChoices.choices,
        default=PayoutAccountChoices.BANK,
    )


    def __str__(self):
        return f"{self.owner.full_name()} - {self.account_type} - Payout Account"
    def save(self, *args, **kwargs):
        extra_data = kwargs.pop("extra_data", {})
        super().save(*args, **kwargs)
        self.create_or_update_related_account(extra_data)
    def create_or_update_related_account(self, extra_data):
        if self.account_type == PayoutAccountChoices.BANK:
            BankAccount.objects.update_or_create(
                payout_account=self,
                defaults={
                    "account_number": extra_data.get("account_number"),
                    "account_name": extra_data.get("account_name"),
                    "bank_name": extra_data.get("bank_name"),
                },
            )
        elif self.account_type == PayoutAccountChoices.PAYPAL:
            PaypalAccount.objects.update_or_create(
                payout_account=self,
                defaults={"email_address": extra_data.get("email_address")},
            )
        elif self.account_type == PayoutAccountChoices.MPESA:
            MpesaAccount.objects.update_or_create(
                payout_account=self,
                defaults={"phone_number": extra_data.get("phone_number")},
            )
        elif self.account_type == PayoutAccountChoices.AIRTEL:
            AirtelAccount.objects.update_or_create(
                payout_account=self,
                defaults={"phone_number": extra_data.get("phone_number")},
            )

    def get_related_account(self):
        """Utility to fetch the related account based on account_type."""
        if self.account_type == PayoutAccountChoices.BANK:
            return getattr(self, "bank_account", None)
        if self.account_type == PayoutAccountChoices.PAYPAL:
            return getattr(self, "paypal_account", None)
        if self.account_type == PayoutAccountChoices.MPESA:
            return getattr(self, "mpesa_account", None)
        if self.account_type == PayoutAccountChoices.AIRTEL:
            return getattr(self, "airtel_account", None)
        return None


class BankAccount(models.Model):
    payout_account = models.OneToOneField(
        PayoutAccount,
        on_delete=models.CASCADE,
        related_name="bank_account",
    )
    account_number = models.PositiveBigIntegerField(blank=True,null=True)
    account_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.account_name} - {self.bank_name} - {self.account_number}"

class PaypalAccount(models.Model):
    payout_account = models.OneToOneField(
        PayoutAccount,
        on_delete=models.CASCADE,
        related_name="paypal_account",
    )
    email_address = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.payout_account.owner.full_name()} - PayPal Account"

class MpesaAccount(models.Model):
    payout_account = models.OneToOneField(
        PayoutAccount,
        on_delete=models.CASCADE,
        related_name="mpesa_account",
    )
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.payout_account.owner.full_name} - MPesa Account"


class AirtelAccount(models.Model):
    payout_account = models.OneToOneField(
        PayoutAccount,
        on_delete=models.CASCADE,
        related_name="airtel_account",
    )
    phone_number = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.payout_account.owner.full_name} - Airtel Account"
