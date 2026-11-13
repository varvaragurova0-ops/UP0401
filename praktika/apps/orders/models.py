from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.catalog.models import Toy
from apps.clients.models import Client

class Order(models.Model):
    class OrderType(models.TextChoices):
        PURCHASE = "purchase", "Покупка"
        PREORDER = "preorder", "Предзаказ"
        RETURN = "return", "Возврат"

    class Status(models.TextChoices):
        NEW = "new", "Новый"
        CONFIRMED = "confirmed", "Подтверждён"
        PAID = "paid", "Оплачен"
        SHIPPED = "shipped", "Отправлен"
        COMPLETED = "completed", "Завершён"
        CANCELLED = "cancelled", "Отменён"

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name="orders", verbose_name="Клиент")
    toy = models.ForeignKey(Toy, on_delete=models.PROTECT, related_name="orders", verbose_name="Игрушка")
    manager = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders", verbose_name="Менеджер")
    order_type = models.CharField("Тип", max_length=20, choices=OrderType.choices)
    quantity = models.PositiveIntegerField("Количество", default=1)
    total_amount = models.DecimalField("Сумма, ₽", max_digits=12, decimal_places=2, default=0)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.NEW)
    comment = models.TextField("Комментарий", blank=True)
    created_at = models.DateTimeField("Создан", auto_now_add=True)
    completed_at = models.DateTimeField("Завершён", null=True, blank=True)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Заказ #{self.pk} — {self.client.full_name}"

    def save(self, *args, **kwargs):
        if not self.pk and self.order_type == self.OrderType.PURCHASE:
            if self.toy.stock >= self.quantity:
                self.toy.stock -= self.quantity
                if self.toy.stock == 0:
                    self.toy.status = Toy.Status.OUT_OF_STOCK
                self.toy.save()
        super().save(*args, **kwargs)

    def complete(self):
        self.status = self.Status.COMPLETED
        self.completed_at = timezone.now()
        self.save()

    def cancel(self):
        self.status = self.Status.CANCELLED
        if self.order_type == self.OrderType.PURCHASE:
            self.toy.stock += self.quantity
            self.toy.status = Toy.Status.AVAILABLE
            self.toy.save()
        self.save()