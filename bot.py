from telebot.util import update_types

from app_init import bot
from app_init import config
from bot_messages_handlers import add_all_handlers
from callback_functions import admin_callbacks
from callback_functions import user_callbacks
from database_interfaces import GroupAdminInterface

add_all_handlers(bot)
while True:
    try:
        bot.polling(allowed_updates = update_types)
    except Exception as ex:
        print(ex)
