from datetime import datetime as dt

from sqlalchemy import and_

from app_init import session
from database_models import Session


class SessionInterface:
    @staticmethod
    def add_new_session(chat_id):
        if not SessionInterface.check_session(chat_id):
            my_session = session()
            session_model = Session(
                chat_id = chat_id
            )
            my_session.add(session_model)
            my_session.commit()

    @staticmethod
    def check_session(chat_id):
        my_session = session()
        return my_session.query(Session).filter(Session.chat_id == chat_id).count() > 0
