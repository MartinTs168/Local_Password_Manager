import sqlite3
from tkinter import Button, Entry
from config_db import conn
from helpers import clean_screen, hash_password
from canvas import root, frame
from main_menu import display_main_menu


def login(username, password):
    # frame.delete('error')
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT password
                FROM users
                WHERE username = :username
            """,
            {"username": username},
        )

        password_from_db = cursor.fetchone()

        if password_from_db is not None:
            password_from_db = password_from_db[0]
        else:
            password_from_db = None
    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()

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


def get_users():
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT username
                FROM users
            """
        )
        info = cursor.fetchall()

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
        return info


def register(username, password, repeat_password):
    info_dict = {
        "username": username,
        "password": password,
        "repeat_password": repeat_password,
    }

    if check_registration(info_dict):
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO users (username, password)
                    VALUES (:username, :password)
                """,
                {
                    "username": info_dict["username"],
                    "password": hash_password(info_dict["password"]),
                },
            )
            conn.commit()
        except sqlite3.Error as e:
            print(e)
        finally:
            cursor.close()

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
        if info["username"] in username:
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
