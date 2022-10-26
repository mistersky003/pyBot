from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

from app_init import bot
from database_interfaces import GroupSettingsInterface
from database_interfaces import KeyboardInterface
from keyboards import generate_group_buttons_types_delete_keyboard


def delete_group_kb_button_callback(chat_id, message_id, call_args):
    if len(call_args):
        if GroupSettingsInterface.check_group_is_exists(call_args[0]):
            bot.delete_message(chat_id, message_id)
            kb = generate_group_buttons_types_delete_keyboard(call_args[0])
            bot.send_message(chat_id, "Выберите тип кнопки, которую следует удалить", reply_markup = kb)
            return
    bot.send_message(chat_id, "Запрос несуществующей группы")
