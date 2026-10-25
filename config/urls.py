"""Глобальные URL-маршруты проекта.

Подключает:
- /admin/  — админка Django
- /api/    — подмаршруты каталога, корзины и авторизации
- /api/docs/  и /api/redoc/  — Swagger и ReDoc (drf-spectacular)
В DEBUG-режиме статика media-файлов раздаётся напрямую.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("catalog.urls")),
    path("api/", include("cart.urls")),
    path("api/", include("accounts.urls")),
    # Документация
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    # Раздача media-файлов только в режиме отладки (DEBUG=True).
    # В продакшене это делает веб-сервер (nginx, Caddy и т.п.).
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
