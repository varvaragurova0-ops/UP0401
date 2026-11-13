from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("client", "toy", "manager").all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "order_type", "client", "toy"]
    search_fields = ["client__full_name", "toy__name"]
    ordering_fields = ["created_at", "total_amount"]

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        order = self.get_object()
        order.complete()
        return Response(OrderSerializer(order).data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        order = self.get_object()
        order.cancel()
        return Response(OrderSerializer(order).data)