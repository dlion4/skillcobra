from django.contrib import admin
from unfold.admin import ModelAdmin

# Register your models here.
from .models import Attendance


@admin.register(Attendance)
class AttendanceAdmin(ModelAdmin):
    list_display = (
        "student",
        "course",
        "attendance_date",
        "present",
        "attendance_counter",
        "notes",
        "created_at",
        "updated_at",
    )
    list_filter = ("course", "student")
    search_fields = ("course", "student")
    ordering = ("-attendance_date",)
    date_hierarchy = "attendance_date"
