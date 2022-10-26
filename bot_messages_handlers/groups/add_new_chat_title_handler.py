from telebot import TeleBot

from database_interfaces import GroupSettingsInterface


def add_new_chat_title_group_messages(bot: TeleBot):
    @bot.message_handler(content_types = ['new_chat_title'])
    def new_chat_title(message):
        if GroupSettingsInterface.check_group_is_exists(message.chat.id):
            GroupSettingsInterface.update_group_settings(message.chat.id, {"group_name": message.chat.title})
        bot.delete_message(message.chat.id, message.message_id)
