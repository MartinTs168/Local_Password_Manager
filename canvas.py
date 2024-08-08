from tkinter import Tk, Canvas


def create_root():
    root = Tk()
    root.title("Password manager")
    root.geometry("800x600")
    root.resizable(False, False)

    return root


def create_frame():
    frame = Canvas(root, width=810, height=610)
    frame.grid(row=0, column=0)
    frame.configure(bg="white")
    frame.configure(borderwidth=-2)

    return frame


root = create_root()
frame = create_frame()
