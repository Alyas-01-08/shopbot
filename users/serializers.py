from django.utils import timezone
from rest_framework import serializers

from utils.service import get_tokens_for_user
from .models import UserBot
from bot.handlers import bot


class UserBotSerializer(serializers.ModelSerializer):
    """ Сериализация данных пользователя
        """
    class Meta:
        model = UserBot
        fields = '__all__'
        extra_kwargs = {'tg_user_id': {
            'read_only': True}, 'id': {'read_only': True}}


class authUserSerializer(serializers.ModelSerializer):
    """
    Авторизация пользователя
    """
    id = serializers.IntegerField(write_only=True)
    refresh = serializers.CharField(read_only=True)
    access = serializers.CharField(read_only=True)

    class Meta:
        model = UserBot
        fields = ('id', 'refresh', 'access',)

    def save(self, **kwargs):
        if user := UserBot.objects.get_or_none(pk=self.validated_data['id']):
            token_data = get_tokens_for_user(user)
            self.validated_data.update(token_data)
        else:
            raise serializers.ValidationError('User not found')
