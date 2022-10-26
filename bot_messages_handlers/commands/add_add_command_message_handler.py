from telebot import TeleBot

from database_interfaces import GroupAdminInterface
from database_interfaces import GroupOwnerInterface
from database_interfaces import GroupSettingsInterface
from database_interfaces import SessionInterface


def add_add_message_handler(bot: TeleBot):
    @bot.message_handler(commands = ['add'])
    def add_group_message(message):
        if SessionInterface.check_session(message.from_user.id):
            bot.delete_message(message.chat.id, message.message_id)
            if message.chat.type != "private":
                if not GroupSettingsInterface.check_group_is_exists(message.chat.id):
                    GroupOwnerInterface.add(message.chat.id, message.from_user.id)
                    GroupSettingsInterface.add_group_settings(message.chat.id)
                    GroupSettingsInterface.update_group_settings(message.chat.id, {
                        "group_name": message.chat.title
                    })
                    bot.send_message(message.chat.id, "Группа успешно добавлена")
                    return
                bot.send_message(message.chat.id, "Группа была добавлена ранее")
                return
            bot.send_message(message.chat.id,
                             "Для добавления группы введите в группе сообщение /add в личных сообщениях это сделать "
                             "невозможно")
        else:
            bot.send_message(message.chat.id, "Для использования бота авторизуйтесь")
