import tkinter as tk
import tkinter.ttk as ttk

from encryption import decrypt


def create_table_with_passwords(root, collection):

    def popup(event):
        from main_menu import edit_menu, delete_password_popup

        menu = tk.Menu(root, tearoff=0)
        menu.add_command(
            label="Edit",
            command=lambda: edit_menu(table.item(table.selection()[0], "values")[0]),
        )
        menu.add_command(
            label="Delete",
            command=lambda: delete_password_popup(
                table.item(table.selection()[0], "values")[0]
            ),
        )

        item = table.identify_row(event.y)
        if item:
            try:
                table.selection_set(item)
                menu.tk_popup(event.x_root, event.y_root)

            finally:
                menu.grab_release()

    table = ttk.Treeview(
        root,
        columns=("id", "service", "username", "email", "password"),
        displaycolumns=("service", "username", "email", "password"),
        show="headings",
        height=50,
    )
    table.heading("id", text="ID")
    table.heading("service", text="Service")
    table.heading("username", text="Username")
    table.heading("email", text="Email")
    table.heading("password", text="Password")

    for obj in collection:
        table.insert(
            "",
            tk.END,
            values=(
                obj.id,
                obj.service,
                obj.username,
                obj.email,
                str(decrypt(obj.password)),
            ),
        )

    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)
    root.columnconfigure(2, weight=1)
    root.columnconfigure(3, weight=1)
    root.columnconfigure(4, weight=1)

    table.grid(row=1, column=0, columnspan=5, sticky="nsew")

    table.bind("<Button-3>", popup)
