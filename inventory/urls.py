from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from .views import CategoryViewSet, ProductViewSet

class HealthCheckView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"})

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"products",  ProductViewSet,  basename="product")

urlpatterns = [
    path("health/", HealthCheckView.as_view(), name="health"),
    path("", include(router.urls)),
]