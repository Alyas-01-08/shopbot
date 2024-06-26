from rest_framework_simplejwt.authentication import JWTAuthentication

from users.models import UserBot


class BotJWTAuthentication(JWTAuthentication):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = UserBot
