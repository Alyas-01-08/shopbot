from telebot import BaseMiddleware
from telebot.types import (
    Message, CallbackQuery
)

from users.models import UserBot
from typing import Union


class AuthMiddleware(BaseMiddleware):
    def __init__(self):
        super(AuthMiddleware, self).__init__()
        self.update_sensitive = False
        self.update_types = ['message', 'callback_query']

    def pre_process(self, message: Union[Message, CallbackQuery], data):
        user_data = message.from_user.to_dict()
        message.u, message.is_created = UserBot.get_user_and_created(user_data)

    def post_process(self, message: Message, data, exception):
        pass
