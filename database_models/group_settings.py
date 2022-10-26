from sqlalchemy import BigInteger
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String

from app_init import base


class GroupSettings(base):
    __tablename__ = "group_settings"
    id = Column(BigInteger, primary_key = True, index = True, nullable = False)
    name = Column(String(255))
    welcome_message = Column(String(1000), default = "Добро пожаловать в группу")
    welcome_message_file_path = Column(String(255))
    welcome_message_is_on = Column(Boolean, default = True)
    number_users_for_invite_for_send_messages = Column(Integer, default = 10)
    number_messages_per_day = Column(Integer, default = 5)
    time_for_send_messages_minutes = Column(Integer, default = 1)
    add_more_users_text = Column(String(1000),
                                 default = "Вы пригласили $count_invited_users\nЧтобы отправлять сообщения в группу "
                                           "нужно добавить $need_count_invite_users")
    reach_max_number_messages_per_day_text = Column(String(1000),
                                                    default = "В день можно отправлять до $max_number_of_messages")
    last_welcome_message_id = Column(BigInteger, default = 0)

    def __str__(self):
        return f"ID: {self.id}\nНазвание группы: {self.name}\nТекст приветственного сообщения: {self.welcome_message}" \
               f"\nКоличество приглашений для написания сообщений в группу: " \
               f"{self.number_users_for_invite_for_send_messages}\nКоличество сообщений в день: " \
               f"{self.number_messages_per_day}\nМинимальное время между отправкой сообщений (минут): " \
               f"{self.time_for_send_messages_minutes}\nОшибка при недостаточном количестве приглашенных " \
               f"пользователей: {self.add_more_users_text}\nОшибка при лимите сообщений: " \
               f"{self.reach_max_number_messages_per_day_text} "
