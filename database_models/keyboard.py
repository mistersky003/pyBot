from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app_init import base


class Keyboard(base):
    __tablename__ = "keyboards"
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    type = Column(String(30), default = "main")
    row_id = Column(Integer, default = 0)
    text = Column(String(120), nullable = False)
    url = Column(String(500), nullable = False)
    group_id = Column(BigInteger, index = True, default = 0)
