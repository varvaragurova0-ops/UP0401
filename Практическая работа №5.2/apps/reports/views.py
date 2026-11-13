from rest_framework.views import APIView
from rest_framework.response import Response
from .services import ReportService

class KPIAPIView(APIView):
    def get(self, request):
        return Response(ReportService.kpi(int(request.GET.get("days", 30))))

class RevenueByDayAPIView(APIView):
    def get(self, request):
        return Response(ReportService.revenue_by_day(int(request.GET.get("days", 30))))

class TopToysAPIView(APIView):
    def get(self, request):
        return Response(ReportService.top_toys(int(request.GET.get("limit", 5))))

class ManagerLoadAPIView(APIView):
    def get(self, request):
        return Response(ReportService.manager_load(int(request.GET.get("days", 30))))

class StockAPIView(APIView):
    def get(self, request):
        return Response(ReportService.stock_status())