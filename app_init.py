from configparser import ConfigParser

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from telebot import TeleBot

config = ConfigParser()
config.read(filenames = "config.ini")
bot = TeleBot(config['BotData']['bot_token'])
base = declarative_base()
engine = create_engine("mysql://root:QAZplmCvbn1!@localhost:3306/bot_secretary")
from database_models import *

if __name__ == "__main__":
    from database_interfaces import AdminInterface
    base.metadata.create_all(engine)
    if not AdminInterface.check_is_exists("admin"):
        AdminInterface.create_admin_model("admin", "admin")

def session():
    engine = create_engine("mysql://root:QAZplmCvbn1!@localhost:3306/bot_secretary")
    session = sessionmaker(bind = engine)
    session = session()
    return session
