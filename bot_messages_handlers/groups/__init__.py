from telebot import TeleBot
from .add_deleted_chat_handlers import add_deleted_group_messages
from .add_new_chat_members_handler import add_new_chat_members_group_messages
from .add_new_chat_title_handler import add_new_chat_title_group_messages
from .add_another_group_messages_handler import add_another_group_messages

def add_group_handlers(bot: TeleBot):
    add_deleted_group_messages(bot)
    add_new_chat_members_group_messages(bot)
    add_new_chat_title_group_messages(bot)
    add_another_group_messages(bot)
