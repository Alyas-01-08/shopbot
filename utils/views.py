from rest_framework.pagination import PageNumberPagination


class GetSerializerClassMixin:

    def get_serializer_class(self):
        """
        A class which inhertis this mixins should have variable
        `serializer_action_classes`.
        Look for serializer class in self.serializer_action_classes, which
        should be a dict mapping action name (key) to serializer class (value),
        i.e.:
        class SampleViewSet(viewsets.ViewSet):
            serializer_class = DocumentSerializer
            serializer_action_classes = {
               'upload': UploadDocumentSerializer,
               'download': DownloadDocumentSerializer,
            }
            @action
            def upload:
                ...
        If there's no entry for that action then just fallback to the regular
        get_serializer_class lookup: self.serializer_class, DefaultSerializer.
        """
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_serializer_class()


class CustomPagination(PageNumberPagination):
    def __init__(self, page_size=10, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_size = page_size
        self.page_size_query_param = 'page_size'
        self.max_page_size = 100
