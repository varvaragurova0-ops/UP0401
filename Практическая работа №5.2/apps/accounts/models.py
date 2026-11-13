from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Кастомный пользователь: роль + телефон."""
    
    class Position(models.TextChoices):
        ADMIN = "admin", "Администратор"
        MANAGER = "manager", "Менеджер"
        CUSTOMER = "customer", "Покупатель"

    phone = models.CharField("Телефон", max_length=20, blank=True)
    position = models.CharField(
        "Роль", max_length=20,
        choices=Position.choices, default=Position.CUSTOMER,
    )

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_position_display()})"