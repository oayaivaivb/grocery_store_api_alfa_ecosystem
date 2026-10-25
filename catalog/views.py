from rest_framework import viewsets
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Только чтение: список категорий с вложенными подкатегориями.

    prefetch_related загружает подкатегории отдельным запросом, чтобы избежать N+1.
    """

    queryset = Category.objects.prefetch_related("subcategories").all()
    serializer_class = CategorySerializer
    lookup_field = "slug"


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Только чтение: список продуктов и детальный просмотр по slug.

    select_related делает JOIN по subcategory→category, чтобы не делать доп. запрос
    при доступе к product.subcategory.category.
    """

    queryset = Product.objects.select_related("subcategory__category").all()
    serializer_class = ProductSerializer
    lookup_field = "slug"
