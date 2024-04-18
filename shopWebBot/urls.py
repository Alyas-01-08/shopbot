from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi, generators
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView


class BothHttpAndHttpsSchemaGenerator(generators.OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["http", 'https']
        return schema


schema_view = get_schema_view(

    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        contact=openapi.Contact(email=""),
        license=openapi.License(name="webtgbot"),

    ),
    generator_class=BothHttpAndHttpsSchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
                                               cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
                                             cache_timeout=0), name='schema-redoc'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('admin/', admin.site.urls),
    path('api-bot/', include('users.urls')),
    path('api/', include('shop.urls')),
    path('api/', include('shoppingCart.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
