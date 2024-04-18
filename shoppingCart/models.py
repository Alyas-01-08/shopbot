from email.policy import default
import uuid
from django.db import models
from shop.models import Product
from users.models import UserBot

from utils.models import CreateUpdateTracker, GetOrNoneManager, nb


class Basket(CreateUpdateTracker):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserBot, on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=30, default='created',
                              choices=(("created", "Создана"), ("canceled", "Отменена"), ("completed", "Завершена")))
    deleted_date = models.DateTimeField(**nb)
    objects = GetOrNoneManager()

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class SelectedProductBasket(CreateUpdateTracker):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='selected_product')
    status = models.CharField('Статус', max_length=30, default='added',
                              choices=(("added", "Новый"), ("deleted", "Удален")))
    basket = models.ForeignKey(
        Basket, on_delete=models.CASCADE, related_name='selected_products_basket')
    size = models.CharField('Размер', max_length=10)
    deleted_date = models.DateTimeField(**nb)
    objects = GetOrNoneManager()

    def __str__(self):
        return f'{self.product.brand.title} - {self.product.title}, size: {self.size}'

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'Товар выделенный в корзину'
        verbose_name_plural = 'Товары выделенные в корзину'


class Order(CreateUpdateTracker):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserBot, on_delete=models.CASCADE)
    total_amount = models.IntegerField('Общая сумма заказа', default=0)
    payment_system = models.CharField('Платежная система', max_length=50, choices=(
        ("visa/mastercard", "Всемирная оплата"), ("rus", "Оплата с России"), ("ton", "Криптовалюта Ton"),
        ("binans", "Binans")), **nb)
    status = models.CharField('Статус', max_length=50, default='creting',
                              choices=(("creting", "Создается"), ("new", "Новый"),
                                       ("waiting", "Ожидает оплаты"), ("paid", "Оплачен"), ("canceled", "Отменен")))
    data = models.JSONField(**nb)
    objects = GetOrNoneManager()

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class SelectedProductOrder(CreateUpdateTracker):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    status = models.CharField('Статус', max_length=30, default='added',
                              choices=(("added", "Новый"), ("deleted", "Удален")))
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='selected_products_order')
    actual_price = models.IntegerField('Актуальная цена')
    size = models.CharField('Размер', max_length=10)
    deleted_date = models.DateTimeField(**nb)
    objects = GetOrNoneManager()

    class Meta:
        ordering = ['created_at', ]
        verbose_name = 'Товар выделенный в заказ'
        verbose_name_plural = 'Товары выделенные в заказ'
