from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "client", "toy", "order_type", "quantity", "total_amount", "status", "created_at")
    list_filter = ("status", "order_type", "created_at")
    search_fields = ("client__full_name", "toy__name")
    readonly_fields = ("created_at", "completed_at")