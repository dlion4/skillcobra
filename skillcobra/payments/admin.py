from django.contrib import admin
from unfold.admin import ModelAdmin

from skillcobra.memberships.models import MemberShip
from skillcobra.memberships.models import Plan
from skillcobra.memberships.models import PlanFeature

from .models import AirtelAccount
from .models import BankAccount
from .models import BillingAddress
from .models import MpesaAccount
from .models import PaymentBalance
from .models import PayoutAccount
from .models import PaypalAccount
from .models import Transaction


@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    list_display = ["name"]


@admin.register(PlanFeature)
class PlanFeatureAdmin(ModelAdmin):
    list_display = ["plan", "feature"]


@admin.register(MemberShip)
class MemberShipAdmin(ModelAdmin):
    list_display = ["profile", "plan"]


@admin.register(Transaction)
class TransactionAdmin(ModelAdmin):
    list_display = [
        "student",
        "parent",
        "status",
        "amount",
        "timestamp",
        "payment_intent",
        "currency",
        "payment_method",
        "reference",
        "payment_reference",
    ]


@admin.register(PaymentBalance)
class PaymentBalanceAdmin(ModelAdmin):
    pass


@admin.register(BillingAddress)
class BillingAddressAdmin(ModelAdmin):
    pass
@admin.register(PayoutAccount)
class PayoutAccountModelAdmin(ModelAdmin):
    pass

@admin.register(BankAccount)
class BankAccountModelAdmin(ModelAdmin):
    pass
@admin.register(PaypalAccount)
class PaypalAccountModelAdmin(ModelAdmin):
    pass
@admin.register(MpesaAccount)
class MpesaAccountModelAdmin(ModelAdmin):
    pass
@admin.register(AirtelAccount)
class AirtelAccountModelAdmin(ModelAdmin):
    pass
