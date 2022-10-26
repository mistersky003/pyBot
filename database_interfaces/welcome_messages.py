from database_models import WelcomeMessage
from app_init import session
from sqlalchemy import and_




class WelcomeMessagesInterface:
    @staticmethod
    def add(group_id, message_id):
        my_session = session()
        if not my_session.query(WelcomeMessage).filter(
                and_(WelcomeMessage.group_id == group_id, WelcomeMessage.message_id == message_id)).count():
            welcome_message = WelcomeMessage(
                group_id = group_id,
                message_id = message_id
            )
            my_session.add(welcome_message)
            my_session.commit()
        return True

    @staticmethod
    def get_messages_without_last(group_id):
        my_session = session()
        messages = my_session.query(WelcomeMessage).filter(WelcomeMessage.group_id == group_id).order_by(
            WelcomeMessage.message_id.desc()).all()
        messages.pop(0)
        return messages


    @staticmethod
    def delete_messages_by_ids(group_id, message_ids):
        my_session = session()
        my_session.query(WelcomeMessage).filter(
            and_(WelcomeMessage.group_id == group_id, WelcomeMessage.message_id.in_(message_ids))).delete()
        my_session.commit()