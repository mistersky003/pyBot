from datetime import datetime as dt

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import BINARY

from app_init import base


class Session(base):
    __tablename__ = "sessions"
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    chat_id = Column(BigInteger, index = True, nullable = False)
