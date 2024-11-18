from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Account
from .models import CourseSale
from .models import ScheduleClass


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
    list_filter = ["holder"]


@admin.register(ScheduleClass)
class ScheduleClassModelAdmin(ModelAdmin):
    list_display = [
        "courses",
        "class_live_link",
        "login_required",
        "lesson_overview",
        "credentials",
        "class_start_time",
        "class_end_time",
        "short_url",
    ]


