from telebot import TeleBot
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup

from database_interfaces import GroupAdminInterface
from database_interfaces import GroupOwnerInterface
from database_interfaces import GroupSettingsInterface
from database_interfaces import SessionInterface
from database_interfaces import KeyboardInterface

from keyboards import generate_auth_keyboard


def add_start_message_handler(bot: TeleBot):
    @bot.message_handler(commands = ['start'])
    def start_message(message):
        if message.chat.type != "private":
            bot.delete_message(message.chat.id, message.message_id)
            return
        if SessionInterface.check_session(message.chat.id):
            user_groups = GroupOwnerInterface.get_user_groups(message.chat.id)
            if len(user_groups):
                count_rows = KeyboardInterface.get_group_keyboard_count_rows(0)
                if count_rows == 0:
                    count_rows = 1
                kb = InlineKeyboardMarkup(row_width = count_rows)
                for user_group in user_groups:
                    group_settings = GroupSettingsInterface.add_group_settings(user_group.group_id)
                    kb.add(
                        InlineKeyboardButton(text = group_settings.name,
                                             callback_data = f"get_group|{group_settings.id}"),
                    )
                if count_rows:
                    for i in range(count_rows):
                        keyboards = KeyboardInterface.get_group_keyboard_row(0, i)
                        keyboard_buttons = []
                        for keyboard_button in keyboards:
                            keyboard_buttons.append(
                                InlineKeyboardButton(text = keyboard_button.text, url = keyboard_button.url)
                            )
                        kb.add(
                            *keyboard_buttons
                        )
                bot.send_message(message.chat.id, "Список ваших групп", reply_markup = kb)
                return
            bot.send_message(message.chat.id, "У вас нет групп")
        else:
            bot.send_message(message.chat.id, "Для использования сервиса войдите в систему",
                             reply_markup = generate_auth_keyboard())
