"""Глобальные фикстуры pytest.

make_image — вспомогательная функция для генерации случайного изображения
в формате JPEG (используется в тестах вместо файлов на диске).
"""

import io

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from catalog.models import Category, Product, Subcategory

User = get_user_model()


@pytest.fixture(autouse=True)
def temp_media(settings, tmp_path):
    """Перенаправляет MEDIA_ROOT во временную папку для каждого теста."""
    settings.MEDIA_ROOT = str(tmp_path)


def make_image(name="test.jpg", size=(1000, 1000)):
    """Создаёт SimpleUploadedFile с одноцветным изображением в памяти."""
    buffer = io.BytesIO()
    Image.new("RGB", size, "#2a9d8f").save(buffer, format="JPEG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/jpeg")


@pytest.fixture
def create_product(db):
    """Фабрика продукта: создаёт категорию, подкатегорию и продукт.

    Может быть вызвана несколько раз — категория и подкатегория не дублируются
    благодаря get_or_create.
    """

    def _create(slug="syr-gauda", name="Сыр Гауда", price="450.00"):
        category, _ = Category.objects.get_or_create(
            slug="molochnye",
            defaults={"name": "Молочные продукты", "image": make_image("cat.jpg")},
        )
        subcategory, _ = Subcategory.objects.get_or_create(
            slug="syry",
            defaults={
                "category": category,
                "name": "Сыры",
                "image": make_image("sub.jpg"),
            },
        )
        return Product.objects.create(
            subcategory=subcategory,
            name=name,
            slug=slug,
            price=price,
            image=make_image(f"{slug}.jpg"),
        )

    return _create


@pytest.fixture
def client(db):
    """Анонимный APIClient."""
    return APIClient()


@pytest.fixture
def user(db):
    """Тестовый пользователь alice."""
    return User.objects.create_user("alice", password="StrongPass12345")


@pytest.fixture
def other_user(db):
    """Второй пользователь bob — для проверки изоляции между пользователями."""
    return User.objects.create_user("bob", password="StrongPass12345")


@pytest.fixture
def auth_client(user):
    """APIClient с авторизацией токеном пользователя user."""
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=user).key}"
    )
    return client


@pytest.fixture
def other_client(other_user):
    """APIClient с авторизацией токеном пользователя other_user."""
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f"Token {Token.objects.create(user=other_user).key}"
    )
    return client
