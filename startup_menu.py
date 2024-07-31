from authentication import login, register
from canvas import root, frame
from tkinter import Button, Entry

from helpers import clean_screen


username_box = Entry(frame, bd=1)
password_box = Entry(frame, bd=1, show="*")
repeat_password_box = Entry(frame, bd=1, show="*")


def clean_input_fields():
    username_box.delete(0, "end")
    password_box.delete(0, "end")
    repeat_password_box.delete(0, "end")


def render_entry():
    clean_screen()
    register_button = Button(
        root,
        text="Register",
        bg="blue",
        fg="white",
        font=("Arial", 11),
        bd=0,
        width=9,
        height=2,
        command=register_menu,
    )

    login_button = Button(
        text="Login",
        bg="lightblue",
        fg="white",
        font=("Arial", 11),
        bd=0,
        width=9,
        height=2,
        command=login_menu,
    )

    frame.create_window(350, 260, window=login_button)
    frame.create_window(350, 310, window=register_button)


back_button = Button(
    frame,
    text="Back",
    bg="darkgrey",
    fg="white",
    font=("Arial", 11),
    bd=0,
    width=9,
    height=2,
    command=render_entry,
)


def register_menu():
    clean_screen()
    clean_input_fields()

    frame.create_text(70, 50, text="Username: ", font=("Arial", 11))
    frame.create_text(70, 100, text="Password: ", font=("Arial", 11))
    frame.create_text(70, 150, text="Repeat password: ", font=("Arial", 11))

    frame.create_window(205, 50, window=username_box)
    frame.create_window(205, 100, window=password_box)
    frame.create_window(205, 150, window=repeat_password_box)

    register_button = Button(
        root,
        text="Register",
        bg="blue",
        fg="white",
        font=("Arial", 11),
        bd=0,
        width=22,
        height=2,
        command=lambda: register(
            username_box.get(), password_box.get(), repeat_password_box.get()
        ),
    )

    frame.create_window(350, 200, window=register_button)
    frame.create_window(350, 310, window=back_button)


def login_menu():
    clean_screen()
    clean_input_fields()

    frame.create_text(70, 50, text="Username: ", font=("Arial", 11))
    frame.create_text(70, 100, text="Password: ", font=("Arial", 11))

    frame.create_window(205, 50, window=username_box)
    frame.create_window(205, 100, window=password_box)

    login_button = Button(
        root,
        text="Login",
        bg="lightblue",
        fg="white",
        font=("Arial", 11),
        bd=0,
        width=22,
        height=2,
        command=lambda: login(username_box.get(), password_box.get()),
    )

    frame.create_window(350, 200, window=login_button)
    frame.create_window(350, 310, window=back_button)
