from django.contrib import admin
from .models import Basket, SelectedProductBasket, Order, SelectedProductOrder


class SelectedProductOrderInline(admin.TabularInline):
    model = SelectedProductOrder
    extra = 0


class SelectedProductBasketInline(admin.TabularInline):
    model = SelectedProductBasket
    extra = 0


@admin.register(Basket)
class BasketAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status')
    list_display_links = ('id',)
    inlines = [SelectedProductBasketInline]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status')
    list_display_links = ('id',)
    inlines = [SelectedProductOrderInline]


admin.site.register(SelectedProductOrder)
admin.site.register(SelectedProductBasket)
