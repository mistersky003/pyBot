from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup




def generate_group_buttons_types_delete_keyboard(group_id):
    kb = InlineKeyboardMarkup(row_width = 1)
    kb.add(
        InlineKeyboardButton(text = "Приветственное сообщение", callback_data = f"delete_kb_bs|{group_id}:main"),
        InlineKeyboardButton(text = "Сообщение об ошибке", callback_data = f"delete_kb_bs|{group_id}:invites"),
        InlineKeyboardButton(text = "Ошибка ограничения постов",
                             callback_data = f"delete_kb_bs|{group_id}:max_mes"),
    )
    return kb