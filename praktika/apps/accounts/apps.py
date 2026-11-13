from django.apps import AppConfig

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"  # <--- ОБЯЗАТЕЛЬНО с apps.
    verbose_name = "Авторизация"