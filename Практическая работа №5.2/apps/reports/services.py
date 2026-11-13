from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from apps.orders.models import Order
from apps.catalog.models import Toy

class ReportService:
    @staticmethod
    def kpi(days: int = 30) -> dict:
        since = timezone.now() - timedelta(days=days)
        completed = Order.objects.filter(
            order_type=Order.OrderType.PURCHASE, status=Order.Status.COMPLETED, created_at__gte=since
        )
        revenue = completed.aggregate(total=Sum("total_amount"))["total"] or 0
        count = completed.count()
        return {
            "revenue": float(revenue), "sales_count": count,
            "avg_check": float(revenue) / count if count else 0,
            "in_stock": Toy.objects.filter(status=Toy.Status.AVAILABLE, stock__gt=0).count(),
            "period_days": days,
        }

    @staticmethod
    def revenue_by_day(days: int = 30) -> list:
        since = timezone.now() - timedelta(days=days)
        rows = (Order.objects.filter(
            order_type=Order.OrderType.PURCHASE, status=Order.Status.COMPLETED, created_at__gte=since
        ).extra(select={"day": "DATE(created_at)"}).values("day").annotate(total=Sum("total_amount")).order_by("day"))
        return [{"date": str(r["day"]), "total": float(r["total"])} for r in rows]

    @staticmethod
    def top_toys(limit: int = 5) -> list:
        rows = (Order.objects.filter(
            order_type=Order.OrderType.PURCHASE, status=Order.Status.COMPLETED
        ).values("toy__brand__name", "toy__name").annotate(count=Count("id")).order_by("-count")[:limit])
        return [{"brand": r["toy__brand__name"], "name": r["toy__name"], "count": r["count"]} for r in rows]

    @staticmethod
    def manager_load(days: int = 30) -> list:
        since = timezone.now() - timedelta(days=days)
        rows = (Order.objects.filter(
            order_type=Order.OrderType.PURCHASE, created_at__gte=since
        ).values("manager__username").annotate(count=Count("id"), total=Sum("total_amount")))
        return [{"manager": r["manager__username"], "orders": r["count"], "total": float(r["total"] or 0)} for r in rows]

    @staticmethod
    def stock_status() -> list:
        return [{"status": r["status"], "count": r["count"]} for r in Toy.objects.values("status").annotate(count=Count("id"))]