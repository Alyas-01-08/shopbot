from telebot import types
from telebot.types import MenuButtonWebApp

from bot.init_bot import bot


def webAppKeyboard():  # создание клавиатуры с webapp кнопкой
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # создаем клавиатуру
    webAppTest = types.WebAppInfo("https://telegram.mihailgok.ru")  # создаем webappinfo - формат хранения url
    one_butt = types.InlineKeyboardButton(text="Тестовая страница", web_app=webAppTest)  # создаем кнопку типа webapp
    keyboard.add(one_butt)  # добавляем кнопки в клавиатуру

    return keyboard  # возвращаем клавиатуру


@bot.message_handler(commands=['start'])
def start(message):
    menu_btn = MenuButtonWebApp('web_app', 'Подписаться', types.WebAppInfo("https://telegram.mihailgok.ru"))
    bot.send_message(message.chat.id, "Тестовая клавиатура", reply_markup=webAppKeyboard())
    bot.set_chat_menu_button(message.chat.id, menu_btn)
