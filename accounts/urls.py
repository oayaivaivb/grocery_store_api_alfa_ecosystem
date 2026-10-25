"""URL-маршруты авторизации.

Эндпоинты:
  /auth/register/  — POST регистрация, возвращает токен
  /auth/login/     — POST вход, возвращает токен
"""

from django.urls import path
from .views import RegisterView, LoginView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
]
