import sqlite3
import tkinter as tk

from tkinter import messagebox
from encryption import decrypt
from helpers import clean_screen
from config_db import conn
from canvas import frame, root

# from table import Table
from models import (
    add_password,
    get_password,
    get_user_through_password,
    edit_password,
    delete_password,
)
from table_treeview import create_table_with_passwords


def display_main_menu(username):
    clean_screen()
    display_passwords(username)
    display_controls(username)


def delete_password_popup(password_id: int):
    msg_box = tk.messagebox.askquestion(
        "Delete Password",
        "Are you sure you want to delete this password?",
        icon="warning",
    )

    if msg_box == "yes":
        app_user = get_user_through_password(password_id)
        delete_password(password_id)
        display_main_menu(app_user.username)


def add_password_menu(app_user):
    clean_screen()

    service_box = tk.Entry(root, bd=1)
    username_box = tk.Entry(root, bd=1)
    email_box = tk.Entry(root, bd=1)
    password_box = tk.Entry(root, bd=1)

    frame.create_text(70, 50, text="Service: ", font=("Arial", 11))
    frame.create_text(70, 100, text="Username: ", font=("Arial", 11))
    frame.create_text(70, 150, text="Email: ", font=("Arial", 11))
    frame.create_text(70, 200, text="Password: ", font=("Arial", 11))

    frame.create_window(205, 50, window=service_box)
    frame.create_window(205, 100, window=username_box)
    frame.create_window(205, 150, window=email_box)
    frame.create_window(205, 200, window=password_box)

    add_button = tk.Button(
        root,
        bg="lightblue",
        fg="white",
        font=("Arial", 11),
        bd=0,
        width=9,
        height=2,
        text="Add",
        command=lambda: (
            add_password_and_redirect(
                app_user,
                service_box.get(),
                username_box.get(),
                email_box.get(),
                password_box.get(),
            )
            if check_fields(
                service_box.get(),
                password_box.get(),
            )
            else None
        ),
    )
    go_back_button = tk.Button(
        root,
        bg="darkgrey",
        fg="white",
        font=("Arial", 11),
        bd=0,
        width=9,
        height=2,
        text="Go Back",
        command=lambda: display_main_menu(app_user),
    )

    frame.create_window(350, 260, window=add_button)
    frame.create_window(350, 310, window=go_back_button)


def edit_menu(password_id: int):
    clean_screen()

    password_obj = get_password(password_id)
    user = get_user_through_password(password_id)

    service_box = tk.Entry(root, bd=1, width=25)
    username_box = tk.Entry(root, bd=1, width=25)
    email_box = tk.Entry(root, bd=1, width=25)
    password_box = tk.Entry(root, bd=1, width=25)

    frame.create_text(70, 50, text="Service: ", font=("Arial", 11))
    frame.create_text(70, 100, text="Username: ", font=("Arial", 11))
    frame.create_text(70, 150, text="Email: ", font=("Arial", 11))
    frame.create_text(70, 200, text="Password: ", font=("Arial", 11))

    frame.create_window(205, 50, window=service_box)
    frame.create_window(205, 100, window=username_box)
    frame.create_window(205, 150, window=email_box)
    frame.create_window(205, 200, window=password_box)

    service_box.insert(tk.END, password_obj.service)
    username_box.insert(tk.END, password_obj.username)
    email_box.insert(tk.END, password_obj.email)
    password_box.insert(tk.END, str(decrypt(password_obj.password)))

    edit_button = tk.Button(
        root,
        bg="lightblue",
        fg="white",
        font=("Arial", 11),
        bd=0,
        width=9,
        height=2,
        text="Edit",
        command=lambda: (
            edit_password_and_redirect(
                user.username,
                password_id,
                service_box.get(),
                username_box.get(),
                email_box.get(),
                password_box.get(),
            )
            if check_fields(
                service_box.get(),
                password_box.get(),
            )
            else None
        ),
    )

    go_back_button = tk.Button(
        root,
        bg="darkgrey",
        fg="white",
        font=("Arial", 11),
        bd=0,
        width=9,
        height=2,
        text="Go Back",
        command=lambda: display_main_menu(user.username),
    )
    frame.create_window(350, 260, window=edit_button)
    frame.create_window(350, 310, window=go_back_button)


def list_passwords(username):
    try:
        cursor = conn.cursor()
        cursor.execute(
            """SELECT ps.id, ps.service, ps.username, ps.email, ps.password
                FROM passwords AS ps
                INNER JOIN users ON users.id = ps.user_id
                WHERE users.username = :username
                ORDER BY ps.service;
            """,
            {"username": username},
        )
        info = cursor.fetchall()

    except sqlite3.Error as e:
        print(e)
    finally:
        cursor.close()
        return info  # returns a list of tuples


def display_passwords(username):
    info = list_passwords(username)
    create_table_with_passwords(root, info)


def display_controls(username):

    add_button = tk.Button(
        root,
        bg="lightblue",
        fg="white",
        font=("Arial", 12),
        bd=0,
        width=9,
        height=2,
        text="Add",
        command=lambda: add_password_menu(username),
    )

    logout_button = tk.Button(
        root,
        bg="darkgrey",
        fg="white",
        font=("Arial", 12),
        bd=0,
        width=9,
        height=2,
        text="Logout",
        command=logout,
    )

    add_button.grid(row=0, column=0, sticky="nw", columnspan=2, ipadx=157, ipady=22)
    logout_button.grid(row=0, column=0, sticky="ne", columnspan=2, ipadx=157, ipady=22)


def check_fields(service, password):
    if service == "" or password == "":
        frame.create_text(
            170,
            320,
            tags="error",
            text="Service and passsword fields must be filled",
            fill="red",
            font=("Arial", 11),
        )
        return False

    return True


def logout():
    from startup_menu import render_entry as render_entry

    clean_screen()
    render_entry()


def add_password_and_redirect(app_user, service, username, email, password):
    add_password(app_user, service, username, email, password)
    display_main_menu(app_user)


def edit_password_and_redirect(
    app_user, password_id, service, username, email, password
):
    edit_password(password_id, service, username, email, password)
    display_main_menu(app_user)
