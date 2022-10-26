from app_init import config
from app_init import session
from database_models.group_admin import GroupAdmin


class GroupAdminInterface:
    @staticmethod
    def create(user_id):
        main_session = session()
        group_admin = main_session.query(GroupAdmin).filter(GroupAdmin.user_id == user_id).first()
        if not group_admin:
            group_admin = GroupAdmin(user_id = user_id)
            main_session.add(group_admin)
            main_session.commit()

    @staticmethod
    def delete(user_id):
        main_session = session()
        count_deleted = main_session.query(GroupAdmin).filter(GroupAdmin.user_id == user_id).delete()
        main_session.commit()
        return count_deleted > 0

    @staticmethod
    def check_user_is_admin(user_id):
        main_session = session()
        status = main_session.query(GroupAdmin).filter(GroupAdmin.user_id == user_id).count() > 0
        if str(user_id) in config['BotData']['admins_ids'].split(",") and not status:
            GroupAdminInterface.create(user_id)
            return True
        return status

    @staticmethod
    def get_all_admins():
        main_session = session()
        return main_session.query(GroupAdmin).all()
