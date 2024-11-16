from django.contrib import admin
from unfold.admin import ModelAdmin

from skillcobra.memberships.models import MemberShip
from skillcobra.memberships.models import Plan
from skillcobra.memberships.models import PlanFeature

from .models import Transaction


@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    list_display = ["name"]

@admin.register(PlanFeature)
class PlanFeatureAdmin(ModelAdmin):
    list_display = ["plan","feature"]

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



