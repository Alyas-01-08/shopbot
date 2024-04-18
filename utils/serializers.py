from rest_framework import serializers


class ResponseSerializer(serializers.Serializer):
    status = serializers.BooleanField(required=False)
    message = serializers.CharField(required=True)
    data = serializers.DictField(required=False)
    list = serializers.ListField(required=False)
