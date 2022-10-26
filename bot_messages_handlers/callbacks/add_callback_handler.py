from telebot import TeleBot
from app_init import config
from callback_functions import admin_callbacks
from callback_functions import user_callbacks
from callback_functions import related_callbacks
from database_interfaces import GroupAdminInterface
from database_interfaces import SessionInterface
from keyboards import generate_auth_keyboard


def add_callback_handler(bot: TeleBot):
    @bot.callback_query_handler(func = lambda call: True)
    def callback_message(call):
        message = call.message
        call_data = call.data.split("|")
        call_type = call_data[0]
        call_arguments = []
        if len(call_data) > 1:
            call_arguments = call_data[1].split(":")
        if message.chat.type != "private":
            bot.delete_message(message.chat.id, message.message_id)
            return
        if call_type in admin_callbacks:
            if str(message.chat.id) in config['BotData']['admins_ids'].split(",") and SessionInterface.check_session(
                    message.chat.id):
                admin_callbacks[call_type](message.chat.id, message.message_id, call_arguments)
            else:
                bot.send_message(message.chat.id, "", reply_markup = generate_auth_keyboard())
        if call_type in user_callbacks:
            if SessionInterface.check_session(message.chat.id):
                user_callbacks[call_type](message.chat.id, message.message_id, call_arguments)
            else:
                bot.send_message(message.chat.id, "", reply_markup = generate_auth_keyboard())
        if call_type in related_callbacks:
            related_callbacks[call_type](message.chat.id, message.message_id, call_arguments)
