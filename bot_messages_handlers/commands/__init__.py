from telebot import TeleBot

from .add_add_command_message_handler import add_add_message_handler
from .add_admin_command_message_handler import add_admin_message_handler
from .add_start_command_message_handler import add_start_message_handler


def add_all_commands_handlers(bot: TeleBot):
    add_start_message_handler(bot)
    add_admin_message_handler(bot)
    add_add_message_handler(bot)
