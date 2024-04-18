from telebot import types, TeleBot


class AnswerBot(TeleBot):
    """Класс для ответа на сообщение"""

    def __init__(self, token: str, *args, **kwargs):
        super().__init__(token, *args, **kwargs)

    def answer(self, message: types.Message, text: str, reply_markup: types.InlineKeyboardMarkup = None):
        """Ответ на сообщение"""
        self.send_message(message.chat.id, text=text, reply_markup=reply_markup)

    def edit_answer(self, message: types.Message, text: str, reply_markup: types.InlineKeyboardMarkup = None):
        """Ответ на сообщение"""
        self.edit_message_text(text=text, chat_id=message.chat.id, message_id=message.message_id,
                               reply_markup=reply_markup)

    def answer_photo(self, message: types.Message, photo: str, **kwargs):
        """Ответ на сообщение"""
        self.send_photo(message.chat.id, photo=photo, **kwargs)


def link(value: str, link: str) -> str:
    return f'<a href="{link}">{value}</a>'


def bold(value: str) -> str:
    return f"<b>{value}</b>"


def italic(value: str) -> str:
    return f"<i>{value}</i>"


def spoiler(value: str) -> str:
    return f'<span class="tg-spoiler">{value}</span>'


def code(value: str) -> str:
    return f"<code>{value}</code>"


def pre(value: str) -> str:
    return f"<pre>{value}</pre>"


def pre_language(value: str, language: str) -> str:
    return f'<pre><code class="language-{language}">{value}</code></pre>'


def underline(value: str) -> str:
    return f"<u>{value}</u>"


def strikethrough(value: str) -> str:
    return f"<s>{value}</s>"
