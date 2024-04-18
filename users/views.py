from PIL import Image
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body
from rest_framework import permissions, viewsets, mixins, views
from rest_framework.exceptions import ParseError
from rest_framework.parsers import FileUploadParser

from rest_framework.response import Response
from rest_framework.decorators import action

from utils.views import CustomPagination, GetSerializerClassMixin


from .models import UserBot
from .serializers import UserBotSerializer, authUserSerializer


class UserBotView(GetSerializerClassMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UserBotSerializer
    serializer_action_classes = {
        'auth': authUserSerializer,
        'get_me': UserBotSerializer,

    }
    queryset = UserBot.objects.all()
    model = UserBot
    paginator = CustomPagination(page_size=2)
    test_param = openapi.Parameter(
        'test', openapi.IN_QUERY, description="test manual param", type=openapi.TYPE_BOOLEAN)

    @action(detail=False, methods=['post'], url_path='auth', permission_classes=[permissions.AllowAny])
    def auth(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @swagger_auto_schema(responses={200: UserBotSerializer()}, operation_description="Получить данные пользователя",
                         paginator_inspectors=[])
    @action(detail=False, methods=['get'], url_path='me', permission_classes=[permissions.IsAuthenticated])
    def get_me(self, request):
        return Response(self.get_serializer(request.user).data)

    def list(self, request, **kwargs):
        queryset = self.model.objects.random(request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class FileUploadView(views.APIView):
    parser_classes = [FileUploadParser]
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request, filename, format=None):

        if 'file' not in request.data:
            raise ParseError("Empty content")

        file_obj = request.data['file']

        # try:
        #     img = Image.open(file_obj)
        #     img.verify()
        # except:
        #     raise ParseError("Unsupported image type")
        user = UserBot.objects.get(id=request.user.id)
        user.image.save(filename, file_obj, save=True)
        return Response(status=204)
