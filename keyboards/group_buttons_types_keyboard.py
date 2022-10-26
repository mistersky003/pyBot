from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton



def generate_group_buttons_types_keyboard(group_id):
    kb = InlineKeyboardMarkup(row_width = 1)
    kb.add(
        InlineKeyboardButton(text = "Приветственное сообщение", callback_data = f"add_keyboard_button|{group_id}:main"),
        InlineKeyboardButton(text = "Сообщение об ошибке", callback_data = f"add_keyboard_button|{group_id}:invites"),
        InlineKeyboardButton(text = "Ошибка ограничения постов",
                             callback_data = f"add_keyboard_button|{group_id}:max_mes"),
    )
    return kb