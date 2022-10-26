from app_init import bot
from app_init import session
from database_models import ChatMember
from database_models import GroupOwner
from database_models import GroupSettings
from database_models import Keyboard


def delete_group_callback(chat_id, message_id, call_args):
    if len(call_args):
        bot.delete_message(chat_id, message_id)
        session_main = session()
        count_delete_group_settings = session_main.query(GroupSettings).filter(GroupSettings.id == call_args[0]).delete()
        session_main.query(GroupOwner).filter(GroupOwner.group_id == call_args[0]).delete()
        session_main.query(ChatMember).filter(ChatMember.group_id == call_args[0]).delete()
        session_main.query(Keyboard).filter(Keyboard.group_id == call_args[0]).delete()
        session_main.commit()
        if count_delete_group_settings > 0:
            bot.send_message(chat_id, "✅ Группа успешно удалена")
        else:
            bot.send_message(chat_id, "❗️Не удалось удалить группу")
        return
    bot.send_message(chat_id, "Произошла непредвиденная ошибка")
