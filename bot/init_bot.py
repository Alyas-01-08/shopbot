import logging
import telebot
from telebot import StateMemoryStorage

from bot.middlewares import *
import os
# from dotenv import load_dotenv
import flask
from bot import utils
from django.conf import settings

# load_dotenv()
state_storage = StateMemoryStorage()
TOKEN = settings.TOKEN

bot = utils.AnswerBot(TOKEN, use_class_middlewares=True, parse_mode='HTML', state_storage=state_storage)

telebot.logger.setLevel(logging.DEBUG)
telebot.apihelper.ENABLE_MIDDLEWARE = True

bot.setup_middleware(AuthMiddleware())

WEBHOOK_HOST = os.environ.get('WEBHOOK_HOST')
WEBHOOK_PORT = os.environ.get('WEBHOOK_PORT')
WEBHOOK_LISTEN = os.environ.get('WEBHOOK_LISTEN')

WEBHOOK_URL_PATH = "/botwebhook"


def run_bot_prod(bot):
    app = flask.Flask(__name__)

    @app.route('/', methods=['GET', 'HEAD'])
    def index():
        return ''

    # Process webhook calls
    @app.route(WEBHOOK_URL_PATH, methods=['POST'])
    def webhook():
        if flask.request.headers.get('content-type') == 'application/json':
            json_string = flask.request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            flask.abort(403)

    bot.remove_webhook()

    bot.set_webhook(url=WEBHOOK_HOST + WEBHOOK_URL_PATH)

    app.run(host=WEBHOOK_LISTEN,
            port=WEBHOOK_PORT,
            debug=True)
