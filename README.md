# Inventory API — Django + DRF + JWT

API REST para gestionar **categorías**, **productos** y **movimientos de inventario (IN/OUT)** con autenticación JWT y documentación OpenAPI (Swagger).

> Proyecto de portafolio: preparado para evaluación técnica (endpoints claros, tests, y guía de ejecución en < 5 minutos).

## ✨ Features
- CRUD de **Categorías** y **Productos**
- **Movimientos de stock** (`/products/{id}/move/`): IN / OUT con validaciones
- **JWT** (access/refresh)
- **Filtros**, **búsqueda** y **ordenación** (DRF)
- **Paginación** global (10 ítems)
- **Swagger** en `/api/docs`
- **Tests** con `pytest` y `pytest-django`

## 🧱 Stack
Django · Django REST Framework · SimpleJWT · drf-spectacular · django-filter · Pytest

## 📁 Estructura
```
InventarioAP/
├─ inventory/
│  ├─ models.py
│  ├─ serializers.py
│  ├─ views.py
│  ├─ urls.py
│  └─ tests/
│     ├─ test_health_and_auth.py
│     └─ test_roles_and_movements.py
├─ InventarioAP/
│  ├─ settings.py
│  └─ urls.py
├─ manage.py
├─ requirements.txt  # o requerimientos.txt
├─ README.md
└─ api_test.http     # pruebas rápidas (PyCharm HTTP Client)
```

## ⚙️ Requisitos
- Python **3.11+**
- (Opcional) MySQL 8 — en desarrollo puedes usar **SQLite**

## 🚀 Quickstart (SQLite)
```bash
python -m venv .venv
# Activa el venv
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
- Docs: `http://127.0.0.1:8000/api/docs/`
- Health: `http://127.0.0.1:8000/api/health/`

## 🔐 Auth (JWT)
1) `POST /api/auth/token/` con `{ "username", "password" }`
2) Usa el `access` en el header:
```
Authorization: Bearer <ACCESS_TOKEN>
```

### (Opcional) Botón **Authorize** en Swagger
En `settings.py` → `SPECTACULAR_SETTINGS` añade:
```python
SPECTACULAR_SETTINGS = {
  "TITLE": "Inventory API",
  "DESCRIPTION": "API para gestión de inventario.",
  "VERSION": "1.0.0",
  "SECURITY": [{"BearerAuth": []}],
  "COMPONENTS": {
    "securitySchemes": {
      "BearerAuth": {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
    }
  },
}
```

## 📚 Endpoints
- `GET /api/health/`
- `POST /api/auth/token/` · `POST /api/auth/token/refresh/`
- `GET|POST /api/categories/` · `GET|PUT|PATCH|DELETE /api/categories/{id}/`
- `GET|POST /api/products/` · `GET|PUT|PATCH|DELETE /api/products/{id}/`
- `POST /api/products/{id}/move/` (IN/OUT)
- `GET /api/movements/`

## 🔎 Filtros, búsqueda y ordenación (ejemplos)
```
/api/products/?search=agua&ordering=-price&category=1&is_active=true
```

## 👮 Permisos
- **Lectura**: cualquier usuario **autenticado**
- **Escritura** (POST/PUT/PATCH/DELETE): solo **staff/admin** (`IsAdminOrReadOnly`)

## 🧪 Tests
```bash
pip install pytest pytest-django
pytest -q
```
- Cobertura mínima: health, auth requerida, creación admin, restricción usuario normal, `move_stock` (IN/OUT).

## 🧰 HTTP Client (PyCharm)
Archivo `api_test.http` con logins (admin/usuario), creación de recursos y `move_stock`. Incluye **asserts** y **variables**.

## 🗃️ MySQL (opcional)
- Usar `PyMySQL` si `mysqlclient` falla en Windows:
  - `pip install pymysql`
  - En `__init__.py` del paquete de `settings.py`:
    ```python
    import pymysql
    pymysql.install_as_MySQLdb()
    ```
  - Mantén `ENGINE = 'django.db.backends.mysql'` en `DATABASES`.

## 🐳 Docker
Incluye `Dockerfile` y `docker-compose.yml` para levantar **API + DB** en minutos (pendiente en Roadmap si no se incluyó).

## 📸 Capturas en proceso de creación

## 🧭 Estado
En desarrollo (MVP funcional). Falta: admin registrado, tests, demo data, CI.

## 🗺️ Roadmap corto
- [ ] Registrar modelos en Django Admin
- [ ] Tests (pytest): categorías, productos, permisos, movimientos IN/OUT, filtros
- [ ] Carga de datos demo (fixtures)
- [ ] CI básica (GitHub Actions: lint + tests)

## 📝 Licencia
MIT
