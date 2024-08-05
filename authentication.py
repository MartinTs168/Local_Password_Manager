from helpers import hash_password
from canvas import root, frame
from main_menu import display_main_menu
from models import add_user, get_user_login_password, get_users


def login(username, password):
    # frame.delete('error')
    password_from_db = get_user_login_password(username)
    if password_from_db == hash_password(password):
        display_main_menu(username)
    else:
        frame.create_text(
            170,
            320,
            text="Wrong username or password",
            font=("Arial", 11),
            fill="red",
            tag="error",
        )


def register(username, password, repeat_password):
    info_dict = {
        "username": username,
        "password": password,
        "repeat_password": repeat_password,
    }

    if check_registration(info_dict):
        add_user(info_dict["username"], hash_password(info_dict["password"]))

        display_main_menu(info_dict["username"])


def check_registration(info):
    frame.delete("error")

    for key, value in info.items():
        if not value.strip():
            frame.create_text(
                170,
                320,
                tags="error",
                text=f"{key.capitalize()} cannot be empty",
                font=("Arial", 11),
                fill="red",
            )

            return False

    if info["password"] != info["repeat_password"]:
        frame.create_text(
            170,
            320,
            tags="error",
            text="Mismatch of passwords",
            font=("Arial", 11),
            fill="red",
        )

        return False
    for username in get_users():
        if info["username"] == username[0]:
            frame.create_text(
                170,
                320,
                tags="error",
                text="Username already exists",
                font=("Arial", 11),
                fill="red",
            )

            return False

    return True
