from django.urls import re_path, path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register(r'shopping', views.BasketView, basename='shopping')

urlpatterns = router.urls + [
    path('orders/me/', views.OrderMeVerifyView.as_view(), name='orders_me'),
    path('orders/add/<uuid:basket_id>', views.OrderAddView.as_view(), name='orders_add'),
]
