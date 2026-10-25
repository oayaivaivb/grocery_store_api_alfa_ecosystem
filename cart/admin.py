"""Регистрация корзин в админке Django.

Корзины создаются автоматически из API, поэтому админка нужна только
для отладки и просмотра — создавать их вручную здесь не требуется.
"""

from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Показывает позиции корзины прямо на странице редактирования корзины."""

    model = CartItem
    # extra = 0 — в отличие от подкатегорий в каталоге, пустые формы не нужны:
    # позиции создаёт сам пользователь через API
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Отображение корзины в админке с вложенными позициями."""

    list_display = ("user",)
    inlines = [CartItemInline]
