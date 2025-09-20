from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from .models import Category, Product, InventoryMovement
from .serializers import CategorySerializer, ProductSerializer, InventoryMovementSerializer
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["name"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_fields = ["category", "is_active"]
    search_fields = ["name", "sku"]
    ordering_fields = ["name", "price", "stock", "created_at"]

    @action(detail=True, methods=["post"], url_path="move")
    def move_stock(self, request, pk=None):
        product = self.get_object()
        movement_type = request.data.get("movement_type")
        try:
            quantity = int(request.data.get("quantity", 0))
        except (TypeError, ValueError):
            return Response({"detail": "quantity must be an integer > 0"}, status=400)
        note = request.data.get("note", "")

        if movement_type not in (InventoryMovement.IN, InventoryMovement.OUT):
            return Response({"detail": "movement_type must be IN or OUT"}, status=400)
        if quantity <= 0:
            return Response({"detail": "quantity must be > 0"}, status=400)

        with transaction.atomic():
            if movement_type == InventoryMovement.OUT and product.stock < quantity:
                return Response({"detail": "Insufficient stock"}, status=400)
            InventoryMovement.objects.create(
                product=product,
                movement_type=movement_type,
                quantity=quantity,
                note=note,
                performed_by=request.user if request.user.is_authenticated else None,
            )
            product.stock = product.stock + quantity if movement_type == "IN" else product.stock - quantity
            product.save(update_fields=["stock"])

        return Response(ProductSerializer(product).data, status=200)
