from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("kpi/", views.KPIAPIView.as_view(), name="kpi"),
    path("revenue/", views.RevenueByDayAPIView.as_view(), name="revenue"),
    path("top-toys/", views.TopToysAPIView.as_view(), name="top_toys"),
    path("manager-load/", views.ManagerLoadAPIView.as_view(), name="manager_load"),
    path("stock/", views.StockAPIView.as_view(), name="stock"),
]