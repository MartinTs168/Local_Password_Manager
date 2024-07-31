import sqlite3

conn = sqlite3.connect("manager.db")


def create_tables():
    sql_statements = [
        """CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );""",
        """CREATE TABLE IF NOT EXISTS passwords(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            service TEXT NOT NULL,
            username TEXT,
            email TEXT,
            password TEXT NOT NULL,
            FOREIGN KEY (user_id) 
                REFERENCES users(id)
        );""",
    ]

    try:
        cur = conn.cursor()
        for statement in sql_statements:
            cur.execute(statement)

        conn.commit()
    except sqlite3.Error as e:
        print(e)
    finally:
        cur.close()
