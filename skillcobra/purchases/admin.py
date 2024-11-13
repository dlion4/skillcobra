from django.contrib import admin

# Register your models here.
from unfold.admin import ModelAdmin

from .models import Cart

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = [
        'student',
        'total_price',
        'created_at',
        'updated_at',
    ]