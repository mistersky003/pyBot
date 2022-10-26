from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

from app_init import bot
from database_interfaces import GroupSettingsInterface
from keyboards import generate_main_group_keyboard



def get_group_callback(chat_id, message_id, call_args):
    bot.delete_message(chat_id, message_id)
    if len(call_args):
        if GroupSettingsInterface.check_group_is_exists(call_args[0]):
            group_settings = GroupSettingsInterface.add_group_settings(call_args[0])
            kb = generate_main_group_keyboard(call_args[0])
            bot.send_message(chat_id, str(group_settings), reply_markup = kb)
            return
        else:
            bot.send_message(chat_id, "Запрос несуществующей группы")
    else:
        bot.send_message(chat_id, "Запрос несуществующей группы")
