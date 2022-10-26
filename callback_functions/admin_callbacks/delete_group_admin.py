from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup

from app_init import bot
from database_interfaces import AdminInterface
from keyboards import generate_main_admin_keyboard
from keyboards import generate_text_back_keyboard


def delete_group_admin_step_1(message):
    chat_id = message.chat.id
    if message.text != "🔙 Назад":
        if AdminInterface.delete_admin(message.text):
            bot.send_message(chat_id, "Пользователь успешно удален")
        else:
            bot.send_message(chat_id, "Невозможно удалить несуществующего пользователя")
    kb = generate_main_admin_keyboard()
    bot.send_message(chat_id, "Добро пожаловать в меню администратора", reply_markup = kb)


def delete_group_admin_callback(chat_id, message_id, call_args):
    kb = generate_text_back_keyboard()
    send_message = bot.send_message(chat_id, "Введите username пользователя, которого нужно удалить",
                                    reply_markup = kb)
    bot.register_next_step_handler(send_message, delete_group_admin_step_1)
