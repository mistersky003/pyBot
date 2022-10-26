from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Integer

from app_init import base


class GroupOwner(base):
    __tablename__ = "group_owners"
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    group_id = Column(BigInteger, index = True, nullable = False)
    owner_id = Column(BigInteger, index = True, nullable = False)
