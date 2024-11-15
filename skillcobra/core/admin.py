from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin
from unfold.admin import StackedInline

from .models import Message
from .models import Notification


@admin.register(Message)
class MessageAdmin(ModelAdmin):
    list_display = ["sender", "receiver", "title", "timestamp"]
@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = ["sender", "receiver", "timestamp"]
