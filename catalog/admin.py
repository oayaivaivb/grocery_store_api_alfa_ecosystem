"""Регистрация моделей каталога в админке Django.

Во всех классах используется prepopulated_fields: поле slug заполняется
автоматически из name на стороне браузера (JS), поэтому вводить его вручную
не нужно — это исключает опечатки и невалидные slug'и.
"""

from django.contrib import admin
from .models import Category, Subcategory, Product


class SubcategoryInline(admin.TabularInline):
    """Позволяет создавать и редактировать подкатегории прямо на странице категории."""

    model = Subcategory
    # extra = 1 — показывать одну пустую форму сверху, чтобы добавить
    # подкатегорию можно было сразу при создании категории
    extra = 1
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории: список с названием и slug, поиск и вложенные подкатегории."""

    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    inlines = [SubcategoryInline]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    """Подкатегории как отдельный раздел — нужны, когда категория уже создана."""

    list_display = ("name", "category", "slug")
    # Фильтр по категории в боковой панели. У Product фильтр идёт по
    # subcategory__category — здесь уровень вложенности не нужен, связь прямая
    list_filter = ("category",)
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Продукты: цена и подкатегория в списке, фильтры по категории и подкатегории."""

    list_display = ("name", "subcategory", "price", "slug")
    # Двойной фильтр: сначала по категории верхней модели, затем по подкатегории.
    # Обход через '__' опирается на ту же цепочку, что и select_related во viewset
    list_filter = ("subcategory__category", "subcategory")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
