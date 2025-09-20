import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_health_ok():
    client = APIClient()
    resp = client.get("/api/health/")
    assert resp.status_code == 200
    assert resp.data.get("status") == "ok"

@pytest.mark.django_db
def test_products_requires_auth():
    client = APIClient()
    resp = client.get("/api/products/")
    assert resp.status_code == 401
