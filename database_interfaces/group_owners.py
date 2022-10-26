from sqlalchemy import and_

from app_init import session
from database_models import GroupOwner


class GroupOwnerInterface:
    @staticmethod
    def add(group_id, owner_id):
        main_session = session()
        group_owner = main_session.query(GroupOwner).filter(
            and_(GroupOwner.group_id == group_id, GroupOwner.owner_id == owner_id)).first()
        if group_owner is None:
            owner = GroupOwner(
                group_id = group_id,
                owner_id = owner_id
            )
            main_session.add(owner)
            main_session.commit()
        return group_owner

    @staticmethod
    def delete(group_id, owner_id):
        main_session = session()
        count_deleted = main_session.query(GroupOwner).filter(
            and_(GroupOwner.group_id == group_id, GroupOwner.owner_id == owner_id)).delete()
        main_session.commit()
        return count_deleted > 0

    @staticmethod
    def get_user_groups(owner_id):
        main_session = session()
        user_groups = main_session.query(GroupOwner).filter(GroupOwner.owner_id == owner_id).all()
        return user_groups
