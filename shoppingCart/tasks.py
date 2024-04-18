from itertools import product
from shopWebBot import celery_app
from .models import Order, Basket, SelectedProductOrder


@celery_app.task
def create_order(basket_id, order):
    if basket := Basket.objects.get_or_none(id=basket_id, status="created"):
        if selected_products := basket.selected_products_basket.all():
            for i in selected_products:
                SelectedProductOrder.objects.create(
                    product=i.product, order=order, actual_price=i.product.price, size=i.size)
        basket.status = 'completed'
        basket.save()
        return True
    return False
