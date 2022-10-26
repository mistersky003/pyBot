import validators
from database_interfaces import GroupSettingsInterface
from database_interfaces import KeyboardInterface
from database_interfaces import SessionInterface
from database_interfaces import AdminInterface

from app_init import bot
from app_init import config

from keyboards import generate_text_back_keyboard
from keyboards import generate_main_admin_keyboard
from keyboards import generate_main_group_keyboard
from keyboards import generate_auth_keyboard


def auth_step_2(message, username):
    chat_id = message.chat.id
    if message.text != "🔙 Назад":
        if not SessionInterface.check_session(chat_id):
            if AdminInterface.check_password(username, message.text):
                SessionInterface.add_new_session(chat_id)
                bot.send_message(chat_id, "Вход успешно выполнен")
                return
            else:
                bot.send_message(chat_id, "Пароль введен не верно")
                send_message = bot.send_message(chat_id, "Введите пароль", reply_markup = generate_text_back_keyboard())
                bot.register_next_step_handler(send_message, auth_step_2, username = message.text)
    bot.send_message(chat_id, "Выход")


def auth_step_1(message):
    chat_id = message.chat.id
    if message.text != "🔙 Назад":
        if not SessionInterface.check_session(chat_id):
            if AdminInterface.check_is_exists(message.text):
                send_message = bot.send_message(chat_id, "Введите пароль", reply_markup = generate_text_back_keyboard())
                bot.register_next_step_handler(send_message, auth_step_2, username = message.text)
                return
            else:
                bot.send_message(chat_id, "Ввод неизвестного username")
                auth_callback(chat_id, message.message_id, [])
                return
    bot.send_message(chat_id, "Выход")


def auth_callback(chat_id, message_id, call_args):
    if not SessionInterface.check_session(chat_id):
        send_message = bot.send_message(chat_id, "Введите username пользователя",
                                        reply_markup = generate_text_back_keyboard())
        bot.register_next_step_handler(send_message, auth_step_1)
