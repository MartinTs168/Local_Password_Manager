from tkinter import  Canvas, Entry, StringVar
class Table(Canvas):
    COLS = 4
    COLS_NAMES = ["service", "username", "email", "password"]
    def __init__(self, root, collection, rows):

        super().__init__()
         
        for j in range(Table.COLS):
                value = StringVar()
                value.set(Table.COLS_NAMES[j])
                self.e = Entry(
                    root,
                    width=15, 
                    fg='blue',
                    font=('Arial',11,'bold'),
                    textvariable=value,
                    state='disabled'
                )
                 
                self.e.grid(row=0, column=j)


        # code for creating table
        for i in range(rows):
            for j in range(Table.COLS):
                value = StringVar()
                value.set(collection[i][j])
                self.e = Entry(
                    root,
                    width=30, 
                    fg='blue',
                    font=('Arial',11,'bold'),
                    textvariable=value,
                    state='disabled'
                )
                 
                self.e.grid(row=i + 1, column=j)