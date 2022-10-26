import validators
from database_interfaces import GroupSettingsInterface
from database_interfaces import KeyboardInterface
from database_interfaces import SessionInterface
from app_init import bot
from app_init import config

from keyboards import generate_text_back_keyboard
from keyboards import generate_main_admin_keyboard
from keyboards import generate_main_group_keyboard
from keyboards import generate_auth_keyboard



def add_keyboard_button_step_1(message, group_id, sended_message_id, keyboard_type):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id)
    bot.delete_message(chat_id, sended_message_id)
    if message.text != "🔙 Назад":
        keyboard_rows = message.text.split("|")
        count_true = 0
        count_false = 0
        for row_id in range(len(keyboard_rows)):
            keyboard_row = keyboard_rows[row_id]
            keyboard_buttons = keyboard_row.split(";")
            for keyboard_button in keyboard_buttons:
                status = False
                keyboard_data = keyboard_button.split("*")
                if len(keyboard_data) == 2:
                    if not KeyboardInterface.check_text_kb_is_exists(group_id, keyboard_data[0], keyboard_type):
                        if validators.url(keyboard_data[1]):
                            status = KeyboardInterface.create_keyboard_button(keyboard_data[0], keyboard_data[1],
                                                                              group_id, row_id = row_id,
                                                                              kb_type = keyboard_type)
                if status:
                    count_true += 1
                else:
                    count_false += 1
        bot.send_message(chat_id,
                         f"Количество кнопок успешно добавленных: {count_true}\nКоличество кнопок с ошибками: "
                         f"{count_false}")
    if group_id == 0:
        kb = generate_main_admin_keyboard()
        bot.send_message(message.chat.id, "Добро пожаловать в меню", reply_markup = kb)
    else:
        group_settings = GroupSettingsInterface.add_group_settings(group_id)
        kb = generate_main_group_keyboard(group_id)
        bot.send_message(chat_id, str(group_settings), reply_markup = kb)


def add_keyboard_button_callback(chat_id, message_id, call_args):
    if len(call_args):
        bot.delete_message(chat_id, message_id)
        if (GroupSettingsInterface.check_group_is_exists(call_args[0]) or (
                int(call_args[0]) == 0 and str(chat_id) in config['BotData']['admins_ids'].split(
                ","))) and SessionInterface.check_session(chat_id):
            kb = generate_text_back_keyboard()
            send_message = bot.send_message(chat_id, "Введите название, и url кнопок в формате(Учитывайте звезду между "
                                                     "словами, | между строками кнопки и ; между кнопками в строке):"
                                                     "Название*URL:Название*URL|Название*URL",
                                            reply_markup = kb)
            keyboard_type = "main"
            if len(call_args) > 1:
                keyboard_type = call_args[1]
            bot.register_next_step_handler(send_message, add_keyboard_button_step_1, group_id = int(call_args[0]),
                                           sended_message_id = send_message.message_id, keyboard_type = keyboard_type)
