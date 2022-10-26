from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

from app_init import bot
from database_interfaces import KeyboardInterface


def delete_admin_kb_button_callback(chat_id, message_id, call_args):
    print("Delete admin kb button")
    if len(call_args) == 1:
        KeyboardInterface.delete_keyboard_button(call_args[0])
    count_rows = KeyboardInterface.get_group_keyboard_count_rows(0)
    kb = InlineKeyboardMarkup(row_width = count_rows)
    for i in range(count_rows):
        keyboards = KeyboardInterface.get_group_keyboard_row(0, i)
        keyboard_buttons = []
        for keyboard_button in keyboards:
            keyboard_buttons.append(
                InlineKeyboardButton(text = keyboard_button.text,
                                     callback_data =
                                     f"delete_admin_kb_button|{keyboard_button.id}"))
        kb.add(
            *keyboard_buttons
        )
    bot.delete_message(chat_id, message_id)
    bot.send_message(chat_id, "Выберите кнопку клавиатуры которую вы хотите удалить",
                     reply_markup = kb)
    return
