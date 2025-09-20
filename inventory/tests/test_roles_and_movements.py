import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api():
    return APIClient()

@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin_t", password="admin_pass", is_staff=True, is_superuser=True)

@pytest.fixture
def normal_user(db):
    return User.objects.create_user(username="user_t", password="user_pass")

def get_token(client, username, password):
    resp = client.post("/api/auth/token/", {"username": username, "password": password}, format="json")
    assert resp.status_code == 200
    return resp.data["access"]

@pytest.mark.django_db
def test_admin_crea_categoria_y_producto(api, admin_user):
    token = get_token(api, "admin_t", "admin_pass")
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    r1 = api.post("/api/categories/", {"name": "Bebidas", "description": "Líquidos varios"}, format="json")
    assert r1.status_code == 201
    cat_id = r1.data["id"]

    r2 = api.post("/api/products/", {
        "sku": "SKU-001",
        "name": "Agua 2L",
        "category": cat_id,
        "price": "10.50",
        "stock": 5
    }, format="json")
    assert r2.status_code == 201
    assert r2.data["sku"] == "SKU-001"

@pytest.mark.django_db
def test_user_normal_no_puede_crear(api, normal_user):
    token = get_token(api, "user_t", "user_pass")
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    r = api.post("/api/categories/", {"name": "No debería"}, format="json")
    assert r.status_code == 403
