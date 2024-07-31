from canvas import root
from startup_menu import render_entry
from config_db import create_tables
from encryption import generate_encryption_key

if __name__ == "__main__":
    create_tables()
    generate_encryption_key()
    render_entry()
    root.mainloop()
