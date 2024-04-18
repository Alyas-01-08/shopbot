from django.urls import re_path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register(r'products', views.ProductView, basename='products')
# urlpatterns = [re_path(r'^upload/(?P<filename>[^/]+)$',
#                        views.FileUploadView.as_view())]
urlpatterns = router.urls
