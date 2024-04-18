from django.contrib import admin
from shop.models import Category, Product, Brand, Size, ProdictImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id',)


class ProdictImgInline(admin.TabularInline):
    model = ProdictImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'gender', 'brand', 'category', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ['gender', 'brand', 'category']
    search_fields = ['id', 'title']
    inlines = [ProdictImgInline]
    ordering = ('-created_at',)


admin.site.register(Size)
admin.site.register(ProdictImage)
