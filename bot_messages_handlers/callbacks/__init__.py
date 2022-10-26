from telebot import TeleBot
from .add_callback_handler import add_callback_handler


def add_callbacks_handlers(bot: TeleBot):
    add_callback_handler(bot)