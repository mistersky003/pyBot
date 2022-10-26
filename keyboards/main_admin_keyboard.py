from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton



def generate_main_admin_keyboard():
    kb = InlineKeyboardMarkup(row_width = 1)
    kb.add(
        InlineKeyboardButton(text = "➕ Добавить управляющего группой", callback_data = "add_group_admin"),
        InlineKeyboardButton(text = "➖ Удалить управляющего группой", callback_data = "delete_group_admin"),
        InlineKeyboardButton(text = "📃 Список управляющих группами", callback_data = "list_group_admins"),
        InlineKeyboardButton(text = "➕ Добавить кнопку", callback_data = "add_keyboard_button|0"),
        InlineKeyboardButton(text = "➖ Удалить кнопку", callback_data = "delete_kb_bs|0:main"),
    )
    return kb