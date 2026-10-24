from decimal import Decimal
from rest_framework import serializers
from catalog.models import Product
from .models import CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(source='product.name', read_only=True)
    slug = serializers.CharField(source='product.slug', read_only=True)
    price = serializers.DecimalField(
        source='product.price', max_digits=10, decimal_places=2, read_only=True
    )
    total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ('id', 'product', 'slug', 'price', 'quantity', 'total')

    def get_total(self, obj) -> Decimal:
        return obj.product.price * obj.quantity


class CartItemAddSerializer(serializers.Serializer):
    """Для добавления: передаём slug продукта и количество."""
    product_slug = serializers.SlugRelatedField(
        slug_field='slug', queryset=Product.objects.all()
    )
    quantity = serializers.IntegerField(min_value=1, default=1)


class CartItemUpdateSerializer(serializers.Serializer):
    """Для изменения количества."""
    quantity = serializers.IntegerField(min_value=1)


class CartSerializer(serializers.Serializer):
    items = CartItemSerializer(many=True)
    total_quantity = serializers.IntegerField()
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)