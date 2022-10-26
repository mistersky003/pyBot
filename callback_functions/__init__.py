from .admin_callbacks import *
from .user_callbacks import *
from .related_callbacks import *

admin_callbacks = {
    "add_group_admin": add_group_admin_callback,
    "delete_group_admin": delete_group_admin_callback,
    "list_group_admins": list_group_admins_callback,
    "add_admin_kb_button": add_admin_kb_button_callback,
    "delete_admin_kb_button": delete_admin_kb_button_callback
}
user_callbacks = {
    "get_group": get_group_callback,
    "delete_group": delete_group_callback,
    "add_group_keyboard_button": add_group_kb_button_callback,
    "delete_group_kb_button": delete_group_kb_button_callback,
    "update_group_data": update_group_callback
}


related_callbacks = {
    "add_keyboard_button": add_keyboard_button_callback,
    "delete_kb_bs": delete_keyboard_buttons_callback,
    "delete_kb_b": delete_keyboard_button_callback,
    "login": auth_callback
}
