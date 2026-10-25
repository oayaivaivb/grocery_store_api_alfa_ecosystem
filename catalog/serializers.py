from rest_framework import serializers
from .models import Category, Subcategory, Product
from drf_spectacular.utils import extend_schema_field


class SubcategorySerializer(serializers.ModelSerializer):
    """Сериализатор подкатегории для встраивания в CategorySerializer."""

    class Meta:
        model = Subcategory
        fields = ("id", "name", "slug", "image")


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категории с вложенным списком подкатегорий."""

    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "slug", "image", "subcategories")


class ProductSerializer(serializers.ModelSerializer):
    """Сериализатор продукта.

    Выводит имя категории и подкатегории через CharField с source (read-only),
    а также генерирует абсолютные URL для трёх вариантов изображения.
    """

    category = serializers.CharField(source="subcategory.category.name", read_only=True)
    subcategory = serializers.CharField(source="subcategory.name", read_only=True)
    images = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ("id", "name", "slug", "category", "subcategory", "price", "images")

    @extend_schema_field(serializers.DictField(child=serializers.URLField()))
    def get_images(self, obj):
        """Собирает словарь URL для small / medium / large.

        Если в контексте есть request, urls делаются абсолютными
        (build_absolute_uri), иначе — относительными (область — только локальный сервер).
        """
        request = self.context.get("request")
        urls = {
            "small": obj.image_small.url,
            "medium": obj.image_medium.url,
            "large": obj.image_large.url,
        }
        if request:
            urls = {size: request.build_absolute_uri(url) for size, url in urls.items()}
        return urls
