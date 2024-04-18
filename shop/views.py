from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, viewsets, mixins
from django_filters import rest_framework as filters
from loguru import logger

from rest_framework.response import Response
from rest_framework.decorators import action

from rest_framework.pagination import PageNumberPagination

from utils.views import CustomPagination, GetSerializerClassMixin

from .filters import ProductFilter
from .models import Brand, Product, Category
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, BrandListSerializer


class ProductView(GetSerializerClassMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAdminUser,)
    serializer_class = ProductSerializer
    serializer_action_classes = {
        'category_list': CategorySerializer,
        'get_brand_list_category': BrandListSerializer,
        'get_brand_list': BrandSerializer,
        # 'get_product': ProductSerializer,
        'get_products_list': ProductSerializer,

    }
    model = Product
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    # filterset_fields = ('category', 'gender')
    queryset = Product.objects.all()

    # paginator = CustomPagination(page_size=2)
    @swagger_auto_schema(responses={200: CategorySerializer()}, operation_description="Получить список категорий",
                         paginator_inspectors=[])
    @action(detail=False, methods=['get'], url_path='category_list/', permission_classes=[permissions.AllowAny])
    def category_list(self, request):
        return Response(self.get_serializer(Category.objects.all(), many=True).data)

    @swagger_auto_schema(responses={200: BrandSerializer()},
                         operation_description="Получить список брендов данной категории",
                         paginator_inspectors=[])
    @action(detail=False, methods=['get'], url_path='brand_list/',
            permission_classes=[permissions.AllowAny])
    def get_brand_list(self, request):
        queryset = Brand.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: BrandListSerializer()},
                         operation_description="Получить список брендов данной категории",
                         paginator_inspectors=[])
    @action(detail=False, methods=['get'], url_path='brand_list_category/(?P<cat_id>[^/.]+)',
            permission_classes=[permissions.AllowAny])
    def get_brand_list_category(self, request, cat_id):
        queryset = Brand.objects.filter(category__id=cat_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny],
            pagination_class=CustomPagination, url_path='list')
    def get_products_list(self, request):
        queryset = self.filter_queryset(queryset=self.queryset)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
