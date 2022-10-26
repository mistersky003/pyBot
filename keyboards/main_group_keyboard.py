from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from database_interfaces import GroupSettingsInterface


def generate_main_group_keyboard(group_id):
    group_settings = GroupSettingsInterface.add_group_settings(group_id)
    welcome_message_is_on_text = "Выключить приветственное сообщение"
    if not group_settings.welcome_message_is_on:
        welcome_message_is_on_text = "Включить приветственное сообщение"
    kb = InlineKeyboardMarkup(row_width = 1)
    kb.add(
        InlineKeyboardButton(text = "Текст стартового сообщение ",
                             callback_data = f"update_group_data|{group_id}:welcome_message"),
        InlineKeyboardButton(text = "Сообщение об ошибке",
                             callback_data = f"update_group_data|{group_id}:add_more_users_text"),
        InlineKeyboardButton(text = "Количество приглашений",
                             callback_data = f"update_group_data|{group_id}:"
                                             f"number_users_must"),
        InlineKeyboardButton(text = "Количество постов",
                             callback_data = f"update_group_data|{group_id}:number_mes"),
        InlineKeyboardButton(text = "Текст об ошибке с ограничение постов",
                             callback_data = f"update_group_data|{group_id}:"
                                             f"reach_max_number_mes"),
        InlineKeyboardButton(text = "Изображение стартового сообщения",
                             callback_data = f"update_group_data|{group_id}:"
                                             f"welcome_message_img"),
        InlineKeyboardButton(text = "Добавить кнопку", callback_data = f"add_group_keyboard_button|{group_id}"),
        InlineKeyboardButton(text = "Удалить кнопку",
                             callback_data = f"delete_group_kb_button|{group_id}"),
        InlineKeyboardButton(text = welcome_message_is_on_text,
                             callback_data = f"update_group_data|{group_id}:w_is_on:"
                                             f"{not group_settings.welcome_message_is_on}"),
        InlineKeyboardButton(text = "Удалить группу",
                             callback_data = f"delete_group|{group_id}"),

    )
    return kb