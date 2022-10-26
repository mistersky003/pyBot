from datetime import datetime as dt

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import BINARY

from app_init import base
from bcrypt import hashpw
from bcrypt import checkpw
from bcrypt import gensalt


class Admin(base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key = True, autoincrement = True, nullable = False)
    username = Column(String(255), nullable = False)
    password_hash = Column(BINARY(60))

    def create_password(self, password):
        self.password_hash = hashpw(password.encode("utf-8"), gensalt(12))

    def check_password(self, password):
        return checkpw(password.encode("utf-8"), self.password_hash)
