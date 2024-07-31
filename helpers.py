import hashlib
from canvas import root
from canvas import frame


def clean_screen():
    frame.delete("all")
    for widget in root.winfo_children():
        if widget != frame:
            widget.destroy()


def hash_password(password):
    # create a hash object
    hash_object = hashlib.sha256()
    # convert the password to bytes
    hash_object.update(password.encode())

    return hash_object.hexdigest()
