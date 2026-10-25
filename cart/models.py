from django.conf import settings
from django.db import models
from catalog.models import Product


class Cart(models.Model):
    """Корзина пользователя — одна на аккаунт.

    Связь OneToOne гарантирует, что у каждого пользователя ровно одна корзина.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cart",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def __str__(self):
        return f"Корзина {self.user}"


class CartItem(models.Model):
    """Отдельная позиция в корзине: продукт и количество.

    UniqueConstraint по (cart, product) обеспечивает, что один продукт
    не может быть представлен дважды — при повторном добавлении увеличивается quantity.
    """

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
        verbose_name="Корзина",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name="Продукт",
    )
    quantity = models.PositiveIntegerField("Количество", default=1)

    class Meta:
        verbose_name = "Позиция корзины"
        verbose_name_plural = "Позиции корзины"
        constraints = [
            models.UniqueConstraint(
                fields=["cart", "product"], name="unique_product_in_cart"
            )
        ]

    def __str__(self):
        return f"{self.product} x {self.quantity}"
