from datetime import datetime as dt
from datetime import timedelta as td

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup
from telebot.types import InlineKeyboardButton

from app_init import config
from celery_tasks import delete_message_task
from database_interfaces import GroupAdminInterface, GroupSettingsInterface, ChatMemberInterface, KeyboardInterface


def add_another_group_messages(bot: TeleBot):
    @bot.message_handler(content_types = ['text', 'audio', 'photo', 'document', 'video', 'sticker', 'voice', 'location',
                                          'contact'])
    def another_messages(message):
        if message.chat.type != "private":
            administrators = bot.get_chat_administrators(message.chat.id)
            administrators_ids = []
            for administrator in administrators:
                administrators_ids.append(administrator.user.id)
            if not GroupAdminInterface.check_user_is_admin(
                    message.from_user.id) and not message.from_user.id in administrators_ids:
                if GroupSettingsInterface.check_group_is_exists(group_id = message.chat.id):
                    error_text = False
                    settings = GroupSettingsInterface.add_group_settings(group_id = message.chat.id)
                    member_interface = ChatMemberInterface(group_id = message.chat.id, member_id = message.from_user.id)
                    count_invited_users = member_interface.get_user_count_invited_users()
                    kb = InlineKeyboardMarkup(row_width = 1)
                    keyboard_buttons = []
                    if int(count_invited_users) < int(settings.number_users_for_invite_for_send_messages):
                        error_text = GroupSettingsInterface.get_text(message.chat.id, "add_more_users_text", {
                            "$sender_username": f"@{message.from_user.username}",
                            "$sender_fname": f"{message.from_user.first_name}",
                            "$count_invited_users": count_invited_users
                        })
                        count_rows = KeyboardInterface.get_group_keyboard_count_rows(message.chat.id,
                                                                                     kb_type = "invites")
                        if count_rows == 0:
                            count_rows = 1
                        kb = InlineKeyboardMarkup(row_width = count_rows)
                        for i in range(count_rows):
                            keyboard_buttons = []
                            keyboards = KeyboardInterface.get_group_keyboard_row(message.chat.id, i,
                                                                                 kb_type = "invites")
                            for keyboard_button in keyboards:
                                keyboard_buttons.append(
                                    InlineKeyboardButton(text = keyboard_button.text, url = keyboard_button.url)
                                )
                            if len(keyboard_buttons):
                                kb.add(*keyboard_buttons)
                    if settings.number_messages_per_day <= member_interface.get_chat_member().count_messages:
                        error_text = GroupSettingsInterface.get_text(message.chat.id,
                                                                     "reach_max_number_messages_per_day_text",
                                                                     {
                                                                         "$sender_fname": f"{message.from_user.first_name}",
                                                                         "$sender_username": f"@{message.from_user.username}",
                                                                         "$count_invited_users": count_invited_users
                                                                     })
                        count_rows = KeyboardInterface.get_group_keyboard_count_rows(message.chat.id,
                                                                                     kb_type = "max_mes")
                        if count_rows == 0:
                            count_rows = 1
                        kb = InlineKeyboardMarkup(row_width = count_rows)
                        for i in range(count_rows):
                            keyboards = KeyboardInterface.get_group_keyboard_row(message.chat.id, i,
                                                                                 kb_type = "max_mes")
                            keyboard_buttons = []
                            for keyboard_button in keyboards:
                                keyboard_buttons.append(
                                    InlineKeyboardButton(text = keyboard_button.text, url = keyboard_button.url)
                                )
                            if len(keyboard_buttons):
                                kb.add(*keyboard_buttons)
                        print(keyboard_buttons)
                    #if dt.utcnow() - member_interface.chat_member.last_message_time < td(
                    #        minutes = settings.time_for_send_messages_minutes):
                    #    bot.delete_message(message.chat.id, message.message_id)
                    #    return
                    if error_text:
                        bot.delete_message(message.chat.id, message.message_id)
                        message = bot.send_message(message.chat.id, error_text, reply_markup = kb)
                        delete_message_task.apply_async((message.chat.id, message.message_id,),
                                                        countdown = int(
                                                            config['BotData']['delete_notification_mail_seconds']))
                        return
                    cmi = ChatMemberInterface(message.chat.id, message.from_user.id)
                    cmi.add_message()
