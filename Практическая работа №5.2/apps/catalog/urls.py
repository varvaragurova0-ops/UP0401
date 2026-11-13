from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandViewSet, ToyViewSet

router = DefaultRouter()
router.register("brands", BrandViewSet, basename="brands")
router.register("toys", ToyViewSet, basename="toys")

urlpatterns = [
    path("", include(router.urls)),
]