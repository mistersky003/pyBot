from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton


def generate_auth_keyboard():
    keyboard = InlineKeyboardMarkup(row_width = 1)
    keyboard.add(InlineKeyboardButton(text = "Войти", callback_data = "login|"))
    return keyboard
