from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from decimal import Decimal
User = get_user_model()

class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Category(TimestampedModel):
    name = models.CharField(max_length=120, unique=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.name

class Product(TimestampedModel):
    sku = models.CharField(
        max_length=64,
        unique=True,
        validators=[RegexValidator(r'^[A-Z0-9-]{3,64}$', 'SKU inválido (usa A-Z, 0-9 y guiones).')]
    )
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.sku} — {self.name}"

class InventoryMovement(models.Model):
    IN = "IN"
    OUT = "OUT"
    MOVEMENT_TYPES = [(IN, "IN"), (OUT, "OUT")]

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="movements")
    movement_type = models.CharField(max_length=3, choices=MOVEMENT_TYPES)
    quantity = models.PositiveIntegerField()
    note = models.CharField(max_length=255, blank=True)
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]