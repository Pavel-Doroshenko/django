"""модели пользований"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """фотография пользователей"""
    photo = models.ImageField(
        upload_to="users/%y/%m/%d/", blank=True, null=True, verbose_name="Фотография"
    )
    date_birth = models.DateTimeField(
        blank=True, null=True, verbose_name="Дата рождения"
    )
