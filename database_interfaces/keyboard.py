import validators
from sqlalchemy import and_

from app_init import session
from database_models import Keyboard


class KeyboardInterface:
    @staticmethod
    def create_keyboard_button(text, url, group_id=0, kb_type="main", row_id=0):
        main_session = session()
        if validators.url(url):
            kb = Keyboard(
                type = kb_type,
                text = text,
                url = url,
                group_id = group_id,
                row_id = row_id
            )
            main_session.add(kb)
            main_session.commit()
            return True
        return False

    @staticmethod
    def check_text_kb_is_exists(group_id, text, kb_type):
        main_session = session()
        return main_session.query(Keyboard).filter(
            and_(Keyboard.group_id == group_id, Keyboard.text == text, Keyboard.type == kb_type)).count() > 0

    @staticmethod
    def get_group_keyboard_row(group_id, row_id, kb_type="main"):
        main_session = session()
        kb_buttons = main_session.query(Keyboard).filter(
            and_(Keyboard.group_id == group_id, Keyboard.row_id == row_id, Keyboard.type == kb_type)).all()
        return kb_buttons

    @staticmethod
    def get_group_keyboard_count_rows(group_id, kb_type="main"):
        main_session = session()
        count_rows = main_session.query(Keyboard).filter(
            and_(Keyboard.group_id == group_id, Keyboard.type == kb_type)).distinct().count()
        return count_rows

    @staticmethod
    def delete_keyboard_button(kb_id):
        main_session = session()
        count_buttons = main_session.query(Keyboard).filter(Keyboard.id == kb_id).delete()
        main_session.commit()
        return count_buttons > 0
