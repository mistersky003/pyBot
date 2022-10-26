from datetime import datetime as dt

from sqlalchemy import and_

from app_init import session
from database_models import ChatMember


class ChatMemberInterface:
    def __init__(self, group_id, member_id, inviter_id=0):
        main_session = session()
        self.group_id = group_id
        self.member_id = member_id
        if main_session.query(ChatMember).filter(
                and_(ChatMember.group_id == group_id, ChatMember.member_id == member_id)).count() == 0:
            chat_member = ChatMember(
                group_id = group_id,
                member_id = member_id,
                inviter_id = inviter_id
            )
            main_session.add(chat_member)
            main_session.commit()

    def add_message(self):
        main_session = session()
        chat_member = main_session.query(ChatMember).filter(
            and_(ChatMember.group_id == self.group_id, ChatMember.member_id == self.member_id)).first()
        chat_member.last_message_time = dt.utcnow()
        chat_member.count_messages += 1
        main_session.commit()

    def get_user_count_invited_users(self):
        main_session = session()
        return main_session.query(ChatMember).filter(and_(ChatMember.group_id == self.group_id,
                                                          ChatMember.inviter_id == self.member_id)).count()

    def get_chat_member(self):
        main_session = session()
        if main_session.query(ChatMember).filter(
                and_(ChatMember.group_id == self.group_id, ChatMember.member_id == self.member_id)).count() == 0:
            chat_member = ChatMember(
                group_id = self.group_id,
                member_id = self.member_id
            )
            main_session.add(chat_member)
            main_session.commit()
        return main_session.query(ChatMember).filter(
            and_(ChatMember.group_id == self.group_id, ChatMember.member_id == self.member_id)).first()
