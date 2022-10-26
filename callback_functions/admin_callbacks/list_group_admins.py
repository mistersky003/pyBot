from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

from app_init import bot
from database_interfaces import GroupAdminInterface
from database_interfaces import AdminInterface
from keyboards import generate_main_admin_keyboard


def list_group_admins_callback(chat_id, message_id, call_args):
    group_admins = AdminInterface.get_admins()
    text_message = "Список управляющих группами:\n"
    for group_admin in group_admins:
        text_message += f"Username: {group_admin.username}\n"
    bot.send_message(chat_id, text_message)
    kb = generate_main_admin_keyboard()
    bot.send_message(chat_id, "Добро пожаловать в меню администратора", reply_markup = kb)
