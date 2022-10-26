from app_init import session
from database_models import GroupSettings
from .my_validators import validate_int
from .my_validators import validate_text
from pathlib import Path


class GroupSettingsInterface:
    @staticmethod
    def add_group_settings(group_id):
        main_session = session()
        group_settings = main_session.query(GroupSettings).filter(GroupSettings.id == group_id).first()
        if group_settings is None:
            group_settings = GroupSettings(id = group_id)
            main_session.add(group_settings)
            main_session.commit()
        return group_settings

    @staticmethod
    def update_group_settings(group_id, update_data: dict):
        main_session = session()
        group_settings = GroupSettingsInterface.add_group_settings(group_id)
        can_update_keys = {
            "name": validate_text(update_data.get("group_name"), 255, 1),
            "welcome_message": validate_text(update_data.get("welcome_message"), 500, 1),
            "welcome_message_file_path": (Path(str(update_data.get("welcome_message_file_path"))).is_file(),
                                          str(Path(str(update_data.get("welcome_message_file_path"))))),
            "welcome_message_is_on": (
                update_data.get("welcome_message_is_on") is not None, update_data.get("welcome_message_is_on")),
            "number_users_for_invite_for_send_messages": validate_int(
                update_data.get("number_users_for_invite_for_send_messages")),
            "number_messages_per_day": validate_int(update_data.get("number_messages_per_day")),
            "time_for_send_messages_minutes": validate_int(update_data.get("time_for_send_messages_minutes"),
                                                           minimum = 1, maximum = int(
                    1440 / group_settings.number_messages_per_day)),
            "add_more_users_text": validate_text(update_data.get("add_more_users_text"), 500, 1),
            "reach_max_number_messages_per_day_text": validate_text(
                update_data.get("reach_max_number_messages_per_day_text"), 500, 1),
            "last_welcome_message_id": validate_int(update_data.get("last_welcome_message_id"))
        }
        updated_keys = {}
        for can_update_key in can_update_keys:
            if can_update_keys[can_update_key][0]:
                updated_keys.update({can_update_key: can_update_keys[can_update_key][1]})
        if updated_keys:
            main_session.query(GroupSettings).filter(GroupSettings.id == group_settings.id).update(updated_keys)
            main_session.commit()
        return list(updated_keys.keys())

    @staticmethod
    def delete_group(group_id):
        main_session = session()
        main_session.query(GroupSettings).filter(GroupSettings.id == group_id).delete()
        main_session.commit()

    @staticmethod
    def get_text(group_id, text_type, additional_arguments=None, is_update_arguments=True):
        group_settings = GroupSettingsInterface.add_group_settings(group_id)
        text_types = {
            "welcome_message": group_settings.welcome_message,
            "add_more_users_text": group_settings.add_more_users_text,
            "reach_max_number_messages_per_day_text": group_settings.reach_max_number_messages_per_day_text
        }
        arguments = {
            "$group_name": group_settings.name,
            "$need_count_invite_users": group_settings.number_users_for_invite_for_send_messages,
            "$max_number_of_messages": group_settings.number_messages_per_day
        }
        if type(additional_arguments) == dict:
            for additional_argument in additional_arguments:
                arguments.update({additional_argument: additional_arguments[additional_argument]})
        if text_type in text_types:
            text = text_types[text_type]
            if is_update_arguments:
                for argument in arguments:
                    text = text.replace(str(argument), str(arguments[argument]))
            return text
        return False

    @staticmethod
    def check_group_is_exists(group_id):
        main_session = session()
        return main_session.query(GroupSettings).filter(GroupSettings.id == group_id).count() > 0
