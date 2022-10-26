from app_init import bot
from database_interfaces import GroupSettingsInterface
from app_init import config
from database_interfaces import KeyboardInterface
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from database_interfaces import SessionInterface


def delete_keyboard_buttons_callback(chat_id, message_id, call_args):
    if call_args:
        bot.delete_message(chat_id, message_id)
        if GroupSettingsInterface.check_group_is_exists(call_args[0]) or (
                int(call_args[0]) == 0 and str(chat_id) in config['BotData']['admins_ids'].split(
                ",")) and SessionInterface.check_session(chat_id):
            count_rows = KeyboardInterface.get_group_keyboard_count_rows(call_args[0],
                                                                         kb_type = call_args[1])
            print(count_rows)
            if count_rows == 0:
                count_rows = 1
            kb = InlineKeyboardMarkup(row_width = count_rows)
            for i in range(count_rows):
                keyboard_buttons = []
                keyboards = KeyboardInterface.get_group_keyboard_row(call_args[0], i,
                                                                     kb_type = call_args[1])
                for keyboard_button in keyboards:
                    keyboard_buttons.append(
                        InlineKeyboardButton(text = keyboard_button.text,
                                             callback_data = f"delete_kb_b|{call_args[0]}:{call_args[1]}:"
                                                             f"{keyboard_button.id}")
                    )
                if len(keyboard_buttons):
                    kb.add(*keyboard_buttons)
            bot.send_message(chat_id, "Доступные кнопки", reply_markup = kb)
