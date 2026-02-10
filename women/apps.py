"""Конфигурация приложения"""
from django.apps import AppConfig


class WomenConfig(AppConfig):
    """Класс конфигурации"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "women"
    verbose_name = "Женщины мира"
