from django.contrib import admin

from .models import InstructorPayout


@admin.register(InstructorPayout)
class InstructorPayoutAdmin(admin.ModelAdmin):
    pass
