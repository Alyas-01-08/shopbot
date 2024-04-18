from itertools import product

from django.db.models import Sum
from requests import delete
from rest_framework import serializers

from shop.models import Product
from shop.serializers import ProductListSerializer
from utils.service import get_tokens_for_user
from .models import Order, Basket, SelectedProductBasket, SelectedProductOrder


class SelectedProductBasketSerializers(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = SelectedProductBasket
        fields = ('id', 'product', 'size', 'status', 'deleted_date')


class BasketSerializer(serializers.ModelSerializer):
    """ Сериализация данных Корзины
        """
    selected_products_basket = SelectedProductBasketSerializers(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, obj):
        return obj.selected_products_basket.filter(status="added").aggregate(Sum('product__price')).get('product__price__sum', 0)

    class Meta:
        model = Basket
        fields = ['id', 'user', 'status',
                  'created_at', 'updated_at', 'deleted_date', 'selected_products_basket', 'total_amount']


class SelectedProductOrderSerializers(serializers.ModelSerializer):
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = SelectedProductOrder
        fields = ('id', 'product', 'status', 'actual_price', 'deleted_date')


class OrderSerializer(serializers.ModelSerializer):
    """ Сериализация данных Заказа
        """
    products = SelectedProductOrderSerializers(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()

    def get_total_amount(self, obj):
        obj.total_amount = obj.selected_products_order.filter(status="added").aggregate(Sum('product__price')).get(
            'product__price__sum', 0)
        obj.save()
        return obj.total_amount

    class Meta:
        model = Order
        fields = ['id', 'user', 'status',
                  'created_at', 'updated_at', 'total_amount',
                  'payment_system', 'data', 'products']
