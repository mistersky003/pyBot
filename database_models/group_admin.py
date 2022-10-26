from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Integer

from app_init import base


class GroupAdmin(base):
    __tablename__ = "group_admins"
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    user_id = Column(BigInteger, index = True, nullable = False)
