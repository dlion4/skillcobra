from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.
from .models import Question


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ("parent", "question", "timestamp")
