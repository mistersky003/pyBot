from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup

from app_init import bot
from database_interfaces import AdminInterface
from keyboards import generate_main_admin_keyboard
from keyboards import generate_text_back_keyboard


def add_group_admin_step_2(message, username):
    chat_id = message.chat.id
    if message.text != "🔙 Назад":
        if AdminInterface.create_admin_model(username, message.text):
            bot.send_message(chat_id, "Пользователь успешно создан")
        else:
            bot.send_message(chat_id, "Ошибка при создании пользователя")
    kb = generate_main_admin_keyboard()
    bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = kb)


def add_group_admin_step_1(message):
    chat_id = message.chat.id
    if message.text != "🔙 Назад":
        if not AdminInterface.check_is_exists(message.text):
            send_message = bot.send_message(chat_id, "Введите пароль пользователя")
            bot.register_next_step_handler(send_message, add_group_admin_step_2, username = message.text)
            return
        else:
            bot.send_message(chat_id, "Невозможно создать пользователя, он уже существует")
    kb = generate_main_admin_keyboard()
    bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = kb)


def add_group_admin_callback(chat_id, message_id, call_args):
    kb = generate_text_back_keyboard()
    send_message = bot.send_message(chat_id, "Введите username",
                                    reply_markup = kb)
    bot.register_next_step_handler(send_message, add_group_admin_step_1)
