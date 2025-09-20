from django.contrib import admin
from .models import Category, Product, InventoryMovement

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id","name","created_at","updated_at")
    search_fields = ("name",)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","sku","name","category","price","stock","is_active","created_at")
    list_filter = ("category","is_active")
    search_fields = ("sku","name")

@admin.register(InventoryMovement)
class InventoryMovementAdmin(admin.ModelAdmin):
    list_display = ("id","product","movement_type","quantity","performed_by","created_at")
    list_filter = ("movement_type",)
    search_fields = ("product__name","note")
