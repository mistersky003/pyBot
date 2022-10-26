from datetime import datetime as dt

from sqlalchemy import and_

from app_init import session
from database_models import Admin


class AdminInterface:
    @staticmethod
    def create_admin_model(username, password):
        my_session = session()
        admin_model = my_session.query(Admin).filter(Admin.username == username).first()
        if not admin_model:
            admin_model = Admin(
                username = username
            )
            admin_model.create_password(password)
            my_session.add(admin_model)
            my_session.commit()
        return admin_model

    @staticmethod
    def check_is_exists(username):
        my_session = session()
        return my_session.query(Admin).filter(Admin.username == username).count() > 0

    @staticmethod
    def check_password(username, password):
        my_session = session()
        admin_model = my_session.query(Admin).filter(Admin.username == username).first()
        if admin_model:
            return admin_model.check_password(password)
        return False

    @staticmethod
    def delete_admin(username):
        my_session = session()
        count_delete = my_session.query(Admin).filter(Admin.username == username).delete()
        my_session.commit()
        return count_delete


    @staticmethod
    def get_admins():
        my_session = session()
        return my_session.query(Admin).all()
