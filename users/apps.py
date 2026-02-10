"""Настройка приложения пользователя"""
from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Конфигурация пользователей"""
    default_auto_field = "django.db.models.BigAutoField"
    name = "users"
