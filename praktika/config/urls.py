from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),

    # === МОДУЛЬ 1: АВТОРИЗАЦИЯ ===
    path("api/auth/", include("apps.accounts.urls")),

    # === МОДУЛЬ 2: КАТАЛОГ ===
    path("api/", include("apps.catalog.urls")),

    # === МОДУЛЬ 3: КЛИЕНТЫ ===
    path("api/clients/", include("apps.clients.urls")),

    # === МОДУЛЬ 4: ЗАКАЗЫ ===
    path("api/orders/", include("apps.orders.urls")),

    # === МОДУЛЬ 5: ОТЧЁТЫ ===
    path("api/reports/", include("apps.reports.urls")),

    # DRF-вход через браузер (для тестирования)
    path("api/drf-login/", include("rest_framework.urls")),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)