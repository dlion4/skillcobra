from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Account
from .models import CourseSale


@admin.register(CourseSale)
class CourseSaleAdmin(ModelAdmin):
    list_display = [
        "tutor",
        "timestamp",
        "modified_timestamp",
        "is_cancelled",
    ]
    list_filter = [
        "tutor",
        "is_cancelled",
    ]



@admin.register(Account)
class AccountAdmin(ModelAdmin):
    list_display = [
        "holder",
        "account_balance",
        "intent",
        "intent_reason",
    ]
    list_filter = [
        "holder",
    ]
