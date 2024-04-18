from django.urls import re_path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter(trailing_slash=False)
router.register(r'userbot', views.UserBotView, basename='userbot')
urlpatterns = [re_path(r'^upload/(?P<filename>[^/]+)$',
                       views.FileUploadView.as_view())]
urlpatterns += router.urls
