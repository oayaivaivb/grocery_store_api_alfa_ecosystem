from decimal import Decimal
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Cart, CartItem
from .serializers import (
    CartItemSerializer,
    CartItemAddSerializer,
    CartItemUpdateSerializer,
    CartSerializer,
)


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def build_cart_response(cart):
    items = cart.items.select_related('product')
    total_quantity = sum(i.quantity for i in items)
    total_price = sum((i.product.price * i.quantity for i in items), Decimal('0'))
    return {
        'items': CartItemSerializer(items, many=True).data,
        'total_quantity': total_quantity,
        'total_price': total_price,
    }


class CartView(APIView):
    """GET - состав корзины, DELETE - полная очистка."""
    permission_classes = [IsAuthenticated]

    @extend_schema(responses={200: CartSerializer})
    def get(self, request):
        cart = get_user_cart(request.user)
        return Response(build_cart_response(cart))

    @extend_schema(request=None, responses={204: None})
    def delete(self, request):
        cart = get_user_cart(request.user)
        cart.items.all().delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CartItemAddView(APIView):
    """POST - добавить продукт в корзину."""
    permission_classes = [IsAuthenticated]

    @extend_schema(request=CartItemAddSerializer, responses={201: CartItemSerializer})
    def post(self, request):
        serializer = CartItemAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data['product_slug']
        quantity = serializer.validated_data['quantity']

        cart = get_user_cart(request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, defaults={'quantity': quantity}
        )
        if not created:
            item.quantity += quantity
            item.save()

        return Response(
            CartItemSerializer(item).data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )


class CartItemDetailView(APIView):
    """PATCH - изменить количество, DELETE - удалить позицию."""
    permission_classes = [IsAuthenticated]

    def get_item(self, request, pk):
        # Фильтр по cart__user гарантирует доступ только к своей корзине
        return get_object_or_404(CartItem, pk=pk, cart__user=request.user)

    @extend_schema(request=CartItemUpdateSerializer, responses={200: CartItemSerializer})
    def patch(self, request, pk):
        item = self.get_item(request, pk)
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        item.quantity = serializer.validated_data['quantity']
        item.save()
        return Response(CartItemSerializer(item).data)

    @extend_schema(request=None, responses={204: None})
    def delete(self, request, pk):
        item = self.get_item(request, pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)