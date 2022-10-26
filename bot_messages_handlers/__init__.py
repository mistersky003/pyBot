from telebot import TeleBot

from .commands import add_all_commands_handlers
from .groups import add_group_handlers
from .callbacks import add_callback_handler


def add_all_handlers(bot: TeleBot):
    add_all_commands_handlers(bot)
    add_group_handlers(bot)
    add_callback_handler(bot)
