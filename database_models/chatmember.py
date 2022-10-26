from datetime import datetime as dt

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer

from app_init import base


class ChatMember(base):
    __tablename__ = "chat_members"
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    group_id = Column(BigInteger, index = True, nullable = False)
    member_id = Column(BigInteger, index = True, nullable = False)
    inviter_id = Column(BigInteger, index = True)
    enter_time = Column(DateTime, default = dt.utcnow)
    last_message_time = Column(DateTime, default = dt.utcnow)
    count_messages = Column(Integer, default = 0)
