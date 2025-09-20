from rest_framework import serializers
from .models import Category, Product, InventoryMovement

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at", "updated_at"]

class ProductSerializer(serializers.ModelSerializer):
    category_detail = CategorySerializer(source="category", read_only=True)
    class Meta:
        model = Product
        fields = ["id", "sku", "name", "category", "category_detail",
                  "price", "stock", "is_active", "created_at", "updated_at"]

class InventoryMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryMovement
        fields = ["id", "product", "movement_type", "quantity", "note", "performed_by", "created_at"]
        read_only_fields = ["performed_by", "created_at"]