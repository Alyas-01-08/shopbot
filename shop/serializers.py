from dataclasses import field, fields
from pyexpat import model
from statistics import mode
from rest_framework import serializers
from .models import Product, Category, Brand, ProdictImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Brand
        fields = '__all__'


class BrandListSerializer(serializers.ModelSerializer):
    logo = serializers.ImageField()

    class Meta:
        model = Brand
        fields = ['title', 'logo']


class ProdictImageSerializer(serializers.ModelSerializer):
    img = serializers.ImageField()

    class Meta:
        model = ProdictImage
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    product_img = ProdictImageSerializer(many=True)
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    size = serializers.StringRelatedField(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class ImageSerializer(serializers.Serializer):
    img = serializers.ImageField()


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    # product_img = ProdictImageSerializer(many=True)
    first_img = serializers.SerializerMethodField()

    def get_first_img(self, obj):
        img = obj.product_img.first()
        return ImageSerializer(img).data

    class Meta:
        model = Product
        fields = ['title', 'price', 'category', 'brand', 'gender', 'first_img']
