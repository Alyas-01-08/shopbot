from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets, mixins
from django_filters import rest_framework as filters
from loguru import logger
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView

from shop.models import Product
from shoppingCart.tasks import create_order
from utils.serializers import ResponseSerializer
from utils.views import GetSerializerClassMixin
from .models import Basket, SelectedProductBasket, Order
from .serializers import BasketSerializer, SelectedProductBasketSerializers, OrderSerializer


class BasketView(GetSerializerClassMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = BasketSerializer
    serializer_action_classes = {
        'basket_me': BasketSerializer,
        'add_to_basket': None,
        'update_to_selected_product_basket': SelectedProductBasketSerializers
    }
    model = Basket
    queryset = Basket.objects.all()

    # paginator = CustomPagination(page_size=2)
    @swagger_auto_schema(responses={200: BasketSerializer(), 400: ResponseSerializer()},
                         operation_description="Получить корзин пользователя",
                         paginator_inspectors=[], tags=['basket'])
    @action(detail=False, methods=['get'], url_path='basket/me', permission_classes=[permissions.IsAuthenticated])
    def basket_me(self, request):
        if obj := self.model.objects.get_or_none(user=request.user, status="created"):
            serializer = self.get_serializer(obj)
            return Response(serializer.data)
        else:
            return Response(ResponseSerializer({"status": False, "message": "Корзина пустая"}).data, status=400)

    @swagger_auto_schema(responses={200: BasketSerializer(), 400: ResponseSerializer()},
                         operation_description="Добавить товар в корзину",
                         paginator_inspectors=[], tags=['basket'])
    @action(detail=False, methods=['post'], url_path='add_to_basket/(?P<product_id>[^/.]+)/(?P<size>[^/.]+)',
            permission_classes=[permissions.IsAuthenticated])
    def add_to_basket(self, request, product_id, size):
        if product := Product.objects.get_or_none(id=product_id):
            basket = Basket.objects.get_or_create(user=request.user, status="created")[0]
            if s := product.size.get_or_none(value=size):
                SelectedProductBasket.objects.create(basket=basket, product=product, size=s)
            else:
                return Response(ResponseSerializer({"status": False, "message": "Размер не найден"}).data, status=400)
            return Response(BasketSerializer(basket, context={'request': request}).data)
        else:
            return Response(ResponseSerializer({"status": False, "message": "Товар не найден"}).data, status=400)

    @swagger_auto_schema(responses={200: BasketSerializer(), 400: ResponseSerializer()},
                         operation_description="Удалить или изменить товар в корзине",
                         paginator_inspectors=[], tags=['basket'], methods=['put', 'delete'])
    @action(detail=False, methods=['put', 'delete'], url_path='update_product_basket/(?P<selected_product_id>[^/.]+)',
            permission_classes=[permissions.IsAuthenticated])
    def update_to_selected_product_basket(self, request, selected_product_id):
        if selected_product := SelectedProductBasket.objects.get_or_none(id=selected_product_id):
            if request.method == 'PUT':
                serializer = self.get_serializer(
                    selected_product, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(BasketSerializer(selected_product.basket).data)
            else:
                selected_product.delete()
                return Response(BasketSerializer(selected_product.basket).data)
        else:
            return Response(ResponseSerializer({"status": False, "message": "Товар не найден"}).data, status=400)


# class OrderView(GetSerializerClassMixin, viewsets.GenericViewSet):
#     permission_classes = (permissions.IsAdminUser,)
#     serializer_class = OrderSerializer
#     model = Order
#     queryset = Order.objects.all()
#
#     @swagger_auto_schema(responses={200: OrderSerializer(many=True), 400: ResponseSerializer()},
#                          operation_description="Получить заказы",
#                          paginator_inspectors=[], tags=['order'])
#     @action(detail=False, methods=['get'], url_path='me/', permission_classes=[permissions.IsAuthenticated])
#     def orders_me(self, request):
#         if queryset := self.model.objects.filter(user=request.user):
#             serializer = self.serializer_class(queryset, many=True)
#             return Response(serializer.data)
#         else:
#             return Response(ResponseSerializer({"status": False, "message": "Нету заказов"}).data, status=400)

# @swagger_auto_schema(responses={200: OrderSerializer(), 400: ResponseSerializer()},
#                      operation_description="Добавить товар в заказ", tags=['basket'])
# @action(detail=False, methods=['get'], url_path='add_to_order/(?P<basket_id>[^/.]+)',
#         permission_classes=[permissions.IsAuthenticated])
# def add_to_order(self, request, basket_id):
#     order = Order.objects.create(user=request.user)
#     created_order = None
#     match settings.DEBUG:
#         case True:
#             created_order = create_order(
#                 basket_id=basket_id, order_id=order.id)
#         case False:
#             created_order = create_order.delay(
#                 basket_id=basket_id, order_id=order.id)
#     if created_order:
#         return Response(OrderSerializer(order, context={'request': request}).data)
#     else:
#         return Response(ResponseSerializer({"status": False, "message": "Корзина пустая"}).data, status=400)

class OrderMeVerifyView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={200: ResponseSerializer(), 400: ResponseSerializer()},
                         operation_description="Проверить заказы", tags=['order'])
    def get(self, request):
        if queryset := Order.objects.filter(user=request.user):
            serializer = OrderSerializer(queryset, many=True)
            return Response(
                ResponseSerializer({"status": True, "message": "Есть заказы", "list": serializer.data}).data)
        else:
            return Response(ResponseSerializer({"status": False, "message": "Нету заказов"}).data, status=400)


class OrderAddView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(responses={400: ResponseSerializer()},
                         operation_description="Добавить товар в заказ", tags=['order'])
    def post(self, request, basket_id):
        order = Order.objects.create(user=request.user)
        created_order = None
        match settings.DEBUG:
            case 1:
                created_order = create_order(
                    basket_id=basket_id, order=order)
            case 0:
                created_order = create_order.delay(
                    basket_id=basket_id, order=order)
        if created_order:
            return Response(OrderSerializer(order, context={'request': request}).data)
        else:
            return Response(ResponseSerializer({"status": False, "message": "Корзина пустая"}).data, status=400)
