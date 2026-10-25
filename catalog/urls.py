"""URL-маршруты каталога.

DefaultRouter автоматически генерирует списочные и детальные эндпоинты:
  /categories/  — список категорий
  /categories/<slug>/  — одна категория (lookup_field = slug, см. viewset)
  /products/  — список продуктов (с пагинацией из настроек)
  /products/<slug>/  — один продукт
"""

from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("products", ProductViewSet, basename="product")

urlpatterns = router.urls
