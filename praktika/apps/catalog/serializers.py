from rest_framework import serializers
from .models import Brand, Toy

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "country"]

class ToySerializer(serializers.ModelSerializer):
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    category_display = serializers.CharField(source="get_category_display", read_only=True)
    age_group_display = serializers.CharField(source="get_age_group_display", read_only=True)

    class Meta:
        model = Toy
        fields = [
            "id", "brand", "brand_name", "name", "category", "category_display",
            "age_group", "age_group_display", "price", "stock", "color",
            "material", "status", "status_display", "sku", "description",
            "image", "created_at",
        ]
        read_only_fields = ["created_at"]