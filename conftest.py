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
    """Картинки из тестов пишутся во временную папку."""
    settings.MEDIA_ROOT = str(tmp_path)


def make_image(name='test.jpg', size=(1000, 1000)):
    buffer = io.BytesIO()
    Image.new('RGB', size, '#2a9d8f').save(buffer, format='JPEG')
    return SimpleUploadedFile(name, buffer.getvalue(), content_type='image/jpeg')


@pytest.fixture
def create_product(db):
    def _create(slug='syr-gauda', name='Сыр Гауда', price='450.00'):
        category, _ = Category.objects.get_or_create(
            slug='molochnye',
            defaults={'name': 'Молочные продукты', 'image': make_image('cat.jpg')},
        )
        subcategory, _ = Subcategory.objects.get_or_create(
            slug='syry',
            defaults={'category': category, 'name': 'Сыры', 'image': make_image('sub.jpg')},
        )
        return Product.objects.create(
            subcategory=subcategory, name=name, slug=slug,
            price=price, image=make_image(f'{slug}.jpg'),
        )
    return _create


@pytest.fixture
def client(db):
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user('alice', password='StrongPass12345')


@pytest.fixture
def other_user(db):
    return User.objects.create_user('bob', password='StrongPass12345')


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {Token.objects.create(user=user).key}')
    return client


@pytest.fixture
def other_client(other_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Token {Token.objects.create(user=other_user).key}')
    return client