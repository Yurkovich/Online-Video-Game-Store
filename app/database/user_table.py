import os
import sqlite3

class UserManager:
    def __init__(self, db_name='database.db', folder_path=None):
        if folder_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            folder_path = os.path.abspath(os.path.join(current_dir, os.pardir))
        
        self.db_path = os.path.join(folder_path, db_name)
        self.folder_path = folder_path
        self._create_db()

    def _create_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                     (id INTEGER PRIMARY KEY, email VARCHAR(40) UNIQUE, password VARCHAR(50))''')
        conn.commit()
        conn.close()

    def authenticate_user(self, email, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?",
                  (email, password))
        user = c.fetchone()
        conn.close()
        return user is not None

    def add_user(self, email, password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, password))
            conn.commit()
        except sqlite3.IntegrityError:
            print("User with this email already exists.")
        finally:
            conn.close()

    def update_user_password(self, email, new_password):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
        conn.commit()
        conn.close()

    def update_user_email(self, current_email, new_email):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        try:
            c.execute("UPDATE users SET email=? WHERE email=?", (new_email, current_email))
            conn.commit()
        except sqlite3.IntegrityError:
            print("User with this new email already exists.")
        finally:
            conn.close()

    def delete_user(self, email):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE email=?", (email,))
        conn.commit()
        conn.close()

db_manager = UserManager()