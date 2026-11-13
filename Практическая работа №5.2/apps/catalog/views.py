from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Brand, Toy
from .serializers import BrandSerializer, ToySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["name", "country"]

class ToyViewSet(viewsets.ModelViewSet):
    queryset = Toy.objects.select_related("brand").all()
    serializer_class = ToySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["brand", "category", "age_group", "status"]
    search_fields = ["name", "sku", "brand__name"]
    ordering_fields = ["price", "stock", "created_at"]