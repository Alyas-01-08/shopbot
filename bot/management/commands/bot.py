import logging
from django.core.management.base import BaseCommand
import os
from bot.handlers import bot
from bot.init_bot import run_bot_prod


class Command(BaseCommand):
    """
    Запуск бота
    """

    def handle(self, *args, **options):
        self.stdout.write('Бот запущен')
        DEBUG = os.environ.get('DEBUG', True)
        if DEBUG:
            bot.infinity_polling(logger_level=logging.DEBUG, long_polling_timeout=20)
        else:
            run_bot_prod(bot)
