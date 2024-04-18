from __future__ import annotations

import uuid
import random
from typing import Union, Optional, Tuple, List
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import QuerySet, Manager
from utils.models import CreateUpdateTracker, nb, GetOrNoneManager, CreateTracker
from asgiref.sync import sync_to_async

from shop.models import Product
from loguru import logger


class AdminUserManager(Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_admin=True)


class UserBotManager(GetOrNoneManager):
    def random(self, user, **kwargs) -> List[UserBot]:
        user_to = user.user_from.values_list('user_to_id', flat=True)
        list_users = self.filter(
            **kwargs).exclude(id__in=user_to).exclude(id=user.id)
        random.shuffle(list(list_users))
        return list_users


class UserBot(CreateUpdateTracker):
    id = models.PositiveBigIntegerField(primary_key=True)  # telegram_id
    username = models.CharField(max_length=32, **nb)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, **nb)
    language_code = models.CharField(
        max_length=8, help_text="Telegram client's lang", **nb)
    deep_link = models.CharField(max_length=64, **nb)
    is_blocked_bot = models.BooleanField(default=False)
    is_bot = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    phone = models.CharField(max_length=50, **nb)
    objects = UserBotManager()  # user = User.objects.get_or_none(user_id=<some_id>)
    admins = AdminUserManager()  # User.admins.all()

    def __str__(self):
        return f'@{self.username}' if self.username is not None else f'{self.id}'

    @classmethod
    def get_user_and_created(cls, user_data: dict) -> Tuple[UserBot, bool]:
        """ python-telegram-bot's Update, Context --> User instance """
        data = cls.init_kwargs(user_data)

        u, created = cls.objects.update_or_create(defaults=data, id=data['id'])

        logger.info(f"User {u.tg_str} created: {created}")
        return u, created

    @classmethod
    def init_kwargs(cls, arg_dict):
        model_fields = [f.name for f in cls._meta.get_fields()]
        return {k: v for k, v in arg_dict.items() if k in model_fields}

    @property
    def tg_str(self) -> str:
        if self.username:
            return f'@{self.username}'
        return f"{self.first_name} {self.last_name or ''}"

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    class Meta:
        ordering = ['is_admin', ]
        verbose_name = 'Пользователь Бота'
        verbose_name_plural = 'Пользователи Бота'


class Address(models.Model):
    user = models.ForeignKey(UserBot, on_delete=models.CASCADE)
    city = models.CharField('Город', max_length=50)
    country = models.CharField('Страна', max_length=50)
    postcode = models.CharField('Почтовый индекс', max_length=50)

    def __str__(self) -> str:
        return f'Страна: {self.country}, г.: {self.city}, почт.:{self.postcode}'

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
