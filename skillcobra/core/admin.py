from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin

from .models import Message
from .models import Notification
from .models import ProfanityModel
from .models import Review


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ["sender", "receiver", "title", "timestamp"]


@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ["sender", "receiver", "timestamp"]


@admin.register(Review)
class ReviewAdmin(ModelAdmin):
    list_display = [
        "profile",
        "parent",
        "rating",
        "alert_message",
        "timestamp",
        "profanity_score",
        "is_verified",
    ]


@admin.register(ProfanityModel)
class ProfanityModelAdmin(ModelAdmin):
    list_display = [
        "message",
        "profanity_score",
    ]
