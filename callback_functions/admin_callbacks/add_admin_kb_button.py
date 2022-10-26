import validators
from telebot.types import InlineKeyboardButton
from telebot.types import InlineKeyboardMarkup
from telebot.types import ReplyKeyboardMarkup

from app_init import bot
from database_interfaces import KeyboardInterface

from keyboards import generate_main_admin_keyboard
from keyboards import generate_text_back_keyboard


def add_admin_kb_button_step_1(message):
    chat_id = message.chat.id
    if message.text != "🔙 Назад":
        keyboard_rows = message.text.split("|")
        count_true = 0
        count_false = 0
        for row_id in range(len(keyboard_rows)):
            keyboard_buttons = keyboard_rows[row_id].split(";")
            for keyboard_button in keyboard_buttons:
                keyboard_data = keyboard_button.split("*")
                status = False
                if len(keyboard_data) == 2:
                    if not KeyboardInterface.check_text_kb_is_exists(0, keyboard_data[0]):
                        if validators.url(keyboard_data[1]):
                            status = KeyboardInterface.create_keyboard_button(keyboard_data[0], keyboard_data[1], 0,
                                                                              row_id = row_id)
                if status:
                    count_true += 1
                else:
                    count_false += 1
        bot.send_message(chat_id,
                         f"Количество кнопок успешно добавленных: {count_true}\nКоличество кнопок с ошибками: "
                         f"{count_false}")
    kb = generate_main_admin_keyboard()
    bot.send_message(message.chat.id, "Добро пожаловать в меню", reply_markup = kb)


def add_admin_kb_button_callback(chat_id, message_id, call_args):
    kb = generate_text_back_keyboard()
    send_message = bot.send_message(chat_id, "Введите название, и url кнопок в формате(Учитывайте звезду между "
                                             "словами, | между строками кнопки и ; между кнопками в строке):"
                                             "Название*URL:Название*URL|Название*URL",
                                    reply_markup = kb)
    bot.register_next_step_handler(send_message, add_admin_kb_button_step_1)
