from telebot.types import ReplyKeyboardMarkup




def generate_text_back_keyboard():
    kb = ReplyKeyboardMarkup(row_width = 1, resize_keyboard = True)
    kb.row("🔙 Назад")
    return kb