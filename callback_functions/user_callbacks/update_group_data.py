from telebot.types import ReplyKeyboardMarkup

from app_init import bot
from database_interfaces import GroupSettingsInterface
from keyboards import generate_main_group_keyboard
from keyboards import generate_text_back_keyboard
from pathlib import Path


def update_group_welcome_file_path(message, group_id, send_message_id):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id)
    bot.delete_message(chat_id, send_message_id)
    if message.text != "🔙 Назад":
        file = None
        if message.content_type == "photo":
            file = message.photo[0]
        elif message.content_type == "video":
            file = message.video
        elif message.content_type == "document":
            file = message.document
        else:
            bot.send_message(chat_id, "Отправлен неизвестный файл")
        if file is not None:
            save_dir = Path(Path.cwd(), "files")
            file_info = bot.get_file(file.file_id)
            downloaded_file = bot.download_file(file_info.file_path)
            src = Path(file_info.file_path).name
            save_path = Path(save_dir, src)
            with open(save_path, 'wb') as new_file:
                new_file.write(downloaded_file)
            status = GroupSettingsInterface.update_group_settings(group_id, {"welcome_message_file_path": save_path})
            if "welcome_message_file_path" in status:
                bot.send_message(chat_id, "Данные успешно обновлены")
            else:
                bot.send_message(chat_id, "Не удалось обновить данные")
    group_settings = GroupSettingsInterface.add_group_settings(group_id)
    kb = generate_main_group_keyboard(group_id)
    bot.send_message(chat_id, str(group_settings), reply_markup = kb)


def update_group_step_1(message, group_id, update_type, send_message_id):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id)
    bot.delete_message(chat_id, send_message_id)
    if message.text != "🔙 Назад":
        updated_keys = GroupSettingsInterface.update_group_settings(group_id, {update_type: message.text})
        if not update_type in updated_keys:
            bot.send_message(chat_id, "Не удалось обновить данные, возможно вы ввели не верный формат")
        else:
            bot.send_message(chat_id, "Данные успешно обновлены")
    group_settings = GroupSettingsInterface.add_group_settings(group_id)
    kb = generate_main_group_keyboard(group_id)
    bot.send_message(chat_id, str(group_settings), reply_markup = kb)


def update_group_callback(chat_id, message_id, call_args):
    bot.delete_message(chat_id, message_id)
    if len(call_args) >= 2:
        if GroupSettingsInterface.check_group_is_exists(call_args[0]):
            update_types = {
                "number_users_must": "number_users_for_invite_for_send_messages",
                "number_mes": "number_messages_per_day",
                "reach_max_number_mes": "reach_max_number_messages_per_day_text",
            }
            update_types_messages = {
                "welcome_message": "Введите текст приветственного сообщения",
                "number_users_for_invite_for_send_messages": "Введите количество пользователей, которых нужно "
                                                             "пригласить для отправки сообщений",
                "number_messages_per_day": "Введите максимальное количество сообщений в день",
                "time_for_send_messages_minutes": "Введите минимальное время между отправками сообщений в минутах",
                "add_more_users_text": "Введите ошибку при недостаточном количестве приглашений",
                "reach_max_number_messages_per_day_text": "Введите ошибку при достижении максимального количества "
                                                          "сообщений за день",
            }
            if call_args[1] in update_types:
                call_args[1] = update_types[call_args[1]]
            if call_args[1] in update_types_messages:
                kb = generate_text_back_keyboard()
                send_message = bot.send_message(chat_id, update_types_messages[call_args[1]], reply_markup = kb)
                bot.register_next_step_handler(send_message, update_group_step_1, group_id = call_args[0],
                                               update_type = call_args[1], send_message_id = send_message.id)
                return
            if call_args[1] == "w_is_on":
                welcome_message_is_on = True
                if call_args[2] == "False":
                    welcome_message_is_on = False
                updated_keys = GroupSettingsInterface.update_group_settings(call_args[0],
                                                                            {
                                                                                "welcome_message_is_on":
                                                                                    welcome_message_is_on
                                                                            })
                if "welcome_message_is_on" in updated_keys:
                    bot.send_message(chat_id, "Данные успешно обновлены")
                else:
                    bot.send_message(chat_id, "Не удалось обновить данные")
                group_settings = GroupSettingsInterface.add_group_settings(call_args[0])
                kb = generate_main_group_keyboard(call_args[0])
                bot.send_message(chat_id, str(group_settings), reply_markup = kb)
                return
            elif call_args[1] == "welcome_message_img":
                kb = generate_text_back_keyboard()
                send_message = bot.send_message(chat_id,
                                                "Отправьте сообщение с файлом, который необходимо прикрепить к "
                                                "сообщению",
                                                reply_markup = kb)
                bot.register_next_step_handler(send_message, update_group_welcome_file_path,
                                               group_id = call_args[0], send_message_id = send_message.message_id)
                return
            bot.send_message(chat_id, "Попытка обновления несуществующего параметра")
        else:
            bot.send_message(chat_id, "Запрос несуществующей группы")
    else:
        bot.send_message(chat_id, "Произошла непредвиденная ошибка")
    group_settings = GroupSettingsInterface.add_group_settings(call_args[0])
    kb = generate_main_group_keyboard(call_args[0])
    bot.send_message(chat_id, str(group_settings), reply_markup = kb)
