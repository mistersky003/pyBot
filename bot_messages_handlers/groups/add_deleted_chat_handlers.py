from telebot import TeleBot


def add_deleted_group_messages(bot: TeleBot):
    @bot.message_handler(content_types = ['new_chat_members', 'left_chat_member'])
    def left_chat_members(message):
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            pass
