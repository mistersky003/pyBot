from telebot import TeleBot
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

from app_init import config
from keyboards import generate_main_admin_keyboard
from keyboards import generate_auth_keyboard

from database_interfaces import SessionInterface

def add_admin_message_handler(bot: TeleBot):
    @bot.message_handler(commands = ['admin'])
    def admin_message(message):
        if message.chat.type != "private":
            bot.delete_message(message.chat.id, message.message_id)
            return
        if str(message.chat.id) in config['BotData']['admins_ids'].split(",") and SessionInterface.check_session(
                message.chat.id):
            kb = generate_main_admin_keyboard()
            bot.send_message(message.chat.id, "Добро пожаловать в меню администратора", reply_markup = kb)
        else:
            bot.send_message(message.chat.id, "Доступ к системе есть только у администраторов",
                             reply_markup = generate_auth_keyboard())
