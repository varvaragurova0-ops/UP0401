from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/auth/", include("apps.accounts.urls")),

    path("api/", include("apps.catalog.urls")),

    path("api/clients/", include("apps.clients.urls")),

    path("api/orders/", include("apps.orders.urls")),

    path("api/reports/", include("apps.reports.urls")),

    path("api/drf-login/", include("rest_framework.urls")),
]