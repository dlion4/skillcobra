from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import Feature
from .models import FeatureAccess
from .models import MemberShip
from .models import MembershipCardCapture
from .models import MemberShipPayment

# Register your models here.
from .models import Plan
from .models import PlanFeature
from .models import Question


@admin.register(Question)
class QuestionAdmin(ModelAdmin):
    list_display = ("parent", "question", "timestamp")


@admin.register(MembershipCardCapture)
class MembershipCardCaptureModalAdmin(ModelAdmin):
    pass




@admin.register(MemberShipPayment)
class MemberShipPaymentModalAdmin(ModelAdmin):
    list_display = [
        "user",
        "amount",
        "date_paid",
        "payment_method",
        "subscription",
    ]


@admin.register(Feature)
class FeatureModalAdmin(ModelAdmin):
    pass


@admin.register(FeatureAccess)
class FeatureAccessModalAdmin(ModelAdmin):
    pass
