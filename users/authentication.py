from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed

from users.models import UserBot


class BotJWTAuthentication(JWTAuthentication):
    www_authenticate_realm = "api-bot"
    media_type = "application/json"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = UserBot

    def authenticate(self, request):
        header = self.get_header(request)
        if header is None:
            return None

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)

        return self.get_user(validated_token), validated_token

    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """

        try:
            user_id = validated_token['user_id']
        except KeyError:
            raise InvalidToken(_("Token contained no recognizable user identification"))
        try:
            user = self.user_model.objects.get(**{'pk': user_id})
        except self.user_model.DoesNotExist:
            raise AuthenticationFailed(_("User not found"), code="user_not_found")
        return user
