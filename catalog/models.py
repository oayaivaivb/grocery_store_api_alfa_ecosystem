from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit


class Category(models.Model):
    """Категория товаров (например, «Молочные продукты» или «Овощи и фрукты»)."""

    name = models.CharField("Наименование", max_length=100)
    slug = models.SlugField("Slug", max_length=100, unique=True)
    image = models.ImageField("Изображение", upload_to="categories/")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """Подкатегория — вложенный элемент категории (например, «Сыры» внутри «Молочных продуктов»)."""

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="subcategories",
        verbose_name="Категория",
    )
    name = models.CharField("Наименование", max_length=100)
    slug = models.SlugField("Slug", max_length=100, unique=True)
    image = models.ImageField("Изображение", upload_to="subcategories/")

    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"
        ordering = ["name"]

    def __str__(self):
        return f"{self.category.name} / {self.name}"


class Product(models.Model):
    """Товар из подкатегории.

    Поля image_small / image_medium / image_large — это ImageSpecField:
    готовые изображения разных размеров генерируются лениво (при первом обращении),
    а не при сохранении модели.
    """

    subcategory = models.ForeignKey(
        Subcategory,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="Подкатегория",
    )
    name = models.CharField("Наименование", max_length=200)
    slug = models.SlugField("Slug", max_length=200, unique=True)
    price = models.DecimalField("Цена", max_digits=10, decimal_places=2)
    image = models.ImageField("Изображение", upload_to="products/")

    image_small = ImageSpecField(
        source="image",
        processors=[ResizeToFit(100, 100)],
        format="JPEG",
        options={"quality": 85},
    )
    image_medium = ImageSpecField(
        source="image",
        processors=[ResizeToFit(300, 300)],
        format="JPEG",
        options={"quality": 85},
    )
    image_large = ImageSpecField(
        source="image",
        processors=[ResizeToFit(800, 800)],
        format="JPEG",
        options={"quality": 85},
    )

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def category(self):
        """Вспомогательное свойство: возвращает родительскую категорию через подкатегорию."""
        return self.subcategory.category
