from database_interfaces.chatmember import ChatMemberInterface
from database_interfaces.keyboard import KeyboardInterface
from database_interfaces.group_settings import GroupSettingsInterface
from sqlite3 import connect
from telebot import TeleBot
import pymysql
import json
from datetime import datetime as dt

conn = connect("main.db")

cursor = conn.cursor()

bot = TeleBot("5019596444:AAGXtPw-Bnn3rsPe2bhVitKYkZrORwaP-98")
#Миграция приглашений
data = cursor.execute("SELECT * FROM users")
inserted_data = []
for d in data:
    try:
        inserted_data.append((d[1], 1, d[0], dt.utcnow(), dt.utcnow(), 0))

    except:
       pass
#oot:QAZplmCvbn1!@localhost:3306/bot_secretary
co = pymysql.connect(
    user = "root",
    password = "QAZplmCvbn1!",
    host = "localhost",
    database = "bot_secretary"
)
c = co.cursor()
c.executemany("INSERT INTO chat_members (group_id, member_id, inviter_id, enter_time, last_message_time, count_messages) VALUES (%s, %s, %s, %s, %s, %s)", inserted_data)
co.commit()
# data = cursor.execute("SELECT * FROM groups")
# for d in data:
#     try:
#         name = bot.get_chat(d[0]).title
#         GroupSettingsInterface.add_group_settings(group_id = d[0])
#         GroupSettingsInterface.update_group_settings(group_id = d[0], update_data = {
#             "group_name": name,
#             "welcome_message": d[3],
#             "number_users_for_invite_for_send_messages": d[2],
#             "number_messages_per_day": d[4],
#             "add_more_users_text": d[1],
#             "reach_max_number_messages_per_day_text": d[5]
#         })
#     except:
#         pass

