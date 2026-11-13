from django.contrib import admin
from .models import Brand, Toy

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "created_at")
    search_fields = ("name",)

@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ("brand", "name", "category", "age_group", "price", "stock", "status")
    list_filter = ("brand", "category", "age_group", "status")
    search_fields = ("name", "sku")
    list_editable = ("status", "stock")