from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import MemberShip

# Register your models here.
from .models import Plan
from .models import PlanFeature


@admin.register(Plan)
class PlanAdmin(ModelAdmin):
    list_display = ["name"]

@admin.register(PlanFeature)
class PlanFeatureAdmin(ModelAdmin):
    list_display = ["plan","feature"]

@admin.register(MemberShip)
class MemberShipAdmin(ModelAdmin):
    list_display = ["profile", "plan"]
