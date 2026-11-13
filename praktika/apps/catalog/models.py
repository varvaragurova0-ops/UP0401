from django.db import models
from django.urls import reverse

class Brand(models.Model):
    name = models.CharField("Название", max_length=50, unique=True)
    country = models.CharField("Страна", max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Бренд"
        verbose_name_plural = "Бренды"
        ordering = ["name"]

    def __str__(self):
        return self.name

class Toy(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "available", "В наличии"
        OUT_OF_STOCK = "out_of_stock", "Нет в наличии"
        DISCONTINUED = "discontinued", "Снято с производства"

    class AgeGroup(models.TextChoices):
        AGE_0_3 = "0-3", "0–3 года"
        AGE_3_6 = "3-6", "3–6 лет"
        AGE_6_12 = "6-12", "6–12 лет"
        AGE_12_PLUS = "12+", "12+ лет"

    class Category(models.TextChoices):
        CONSTRUCTOR = "constructor", "Конструктор"
        DOLL = "doll", "Кукла"
        CAR = "car", "Машинка"
        EDUCATIONAL = "educational", "Развивающая"
        SOFT = "soft", "Мягкая игрушка"
        BOARD_GAME = "board_game", "Настольная игра"

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="toys", verbose_name="Бренд")
    name = models.CharField("Название", max_length=100)
    category = models.CharField("Категория", max_length=30, choices=Category.choices)
    age_group = models.CharField("Возраст", max_length=10, choices=AgeGroup.choices)
    price = models.DecimalField("Цена, ₽", max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField("Остаток, шт", default=0)
    color = models.CharField("Цвет", max_length=30, blank=True)
    material = models.CharField("Материал", max_length=50, blank=True)
    status = models.CharField("Статус", max_length=20, choices=Status.choices, default=Status.AVAILABLE)
    sku = models.CharField("Артикул", max_length=20, unique=True, blank=True, null=True)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Фото", upload_to="toys/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Игрушка"
        verbose_name_plural = "Игрушки"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.brand.name} {self.name} ({self.age_group})"

    def get_absolute_url(self):
        return reverse("catalog:toy_detail", args=[self.pk])

    @property
    def is_available(self):
        return self.status == self.Status.AVAILABLE and self.stock > 0