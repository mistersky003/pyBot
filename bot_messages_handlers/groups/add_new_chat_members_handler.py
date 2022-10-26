import os
from pathlib import Path

import magic
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

from database_interfaces import ChatMemberInterface, GroupSettingsInterface, KeyboardInterface, WelcomeMessagesInterface


def add_new_chat_members_group_messages(bot: TeleBot):
    @bot.chat_member_handler()
    @bot.chat_join_request_handler()
    def new_chat_member_message(message):
        inviter_id = 0
        if message.from_user.id != message.new_chat_member.user.id:
            inviter_id = message.from_user.id
        ChatMemberInterface(message.chat.id, message.new_chat_member.user.id, inviter_id = inviter_id)
        if GroupSettingsInterface.check_group_is_exists(group_id = message.chat.id):
            grop_settings = GroupSettingsInterface.add_group_settings(message.chat.id)
            if grop_settings.welcome_message_is_on:
                welcome_message = GroupSettingsInterface.get_text(message.chat.id, "welcome_message",
                                                                  additional_arguments = {
                                                                      "$sender_fname": message.from_user.first_name
                                                                  })

                if welcome_message:
                    count_rows = KeyboardInterface.get_group_keyboard_count_rows(message.chat.id)
                    kb = InlineKeyboardMarkup(row_width = count_rows)
                    if count_rows:
                        for i in range(count_rows):
                            keyboards = KeyboardInterface.get_group_keyboard_row(message.chat.id, i)
                            keyboard_buttons = []
                            for keyboard_button in keyboards:
                                keyboard_buttons.append(
                                    InlineKeyboardButton(text = keyboard_button.text, url = keyboard_button.url)
                                )
                            kb.add(
                                *keyboard_buttons
                            )
                    if os.path.isfile(str(grop_settings.welcome_message_file_path)):
                        file_path = Path(grop_settings.welcome_message_file_path)
                        file_type = magic.from_file(file_path)
                        with open(file_path, 'rb') as file:
                            if "image" in file_type:
                                send_message = bot.send_photo(message.chat.id, photo = file,
                                                              caption = welcome_message, reply_markup = kb)
                            elif "video" in file_type:
                                send_message = bot.send_video(message.chat.id, video = file,
                                                              caption = welcome_message, reply_markup = kb)
                            else:
                                send_message = bot.send_document(message.chat.id, document = file,
                                                                 caption = welcome_message, reply_markup = kb)
                    else:
                        send_message = bot.send_message(message.chat.id, welcome_message, reply_markup = kb)
                    GroupSettingsInterface.update_group_settings(message.chat.id,
                                                                 {"last_welcome_message_id": send_message.id})
                    WelcomeMessagesInterface.add(message.chat.id, send_message.id)
                    messages = WelcomeMessagesInterface.get_messages_without_last(message.chat.id)
                    messages_ids = []
                    for wmessage in messages:
                        messages_ids.append(wmessage.message_id)
                        try:
                            bot.delete_message(chat_id = wmessage.group_id, message_id = wmessage.message_id)
                        except:
                            pass
                    WelcomeMessagesInterface.delete_messages_by_ids(message.chat.id, messages_ids)
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
