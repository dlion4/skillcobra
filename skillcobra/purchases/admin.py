from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin
from django.core.exceptions import ValidationError
from .models import Cart
from .models import Coupon


@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = [
        "student",
        "total_price",
        "created_at",
        "updated_at",
    ]
@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = [
        "course",
        "code",
        "discount_percent",
        "start_timestamp",
        "ended_timestamp",
        "is_active",
    ]
    # exclude = ["code", "students"]
    def save_model(self, request, obj, form, change):
        if obj.course.status != "approved":
            msg = (
                "Can only create coupon code for approved courses. ((#: {obj.title}) not approved)"  # noqa: E501
            )
            raise ValidationError(msg)
        super().save_model(request, obj, form, change)
    def get_queryset(self, request):
        return Coupon.admin_objects.all()

