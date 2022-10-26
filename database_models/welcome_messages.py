from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app_init import base


class WelcomeMessage(base):
    __tablename__ = "welcome_messages"
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    message_id = Column(BigInteger, index = True, default = 0)
    group_id = Column(BigInteger, index = True, default = 0)