import sqlite3

from django.conf import settings


class UserStateManager:
    def __init__(self):
        self.db_path = settings.DATABASES['default']['NAME']
        self.previous_states = {}

    def create_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_state (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                state TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_user_state(self, user_id, state):
        # Получите предыдущее состояние, если оно есть
        previous_state = self.previous_states.get(user_id)

        # Сохраните текущее состояние как предыдущее
        self.previous_states[user_id] = state

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_state (user_id, state) VALUES (?, ?)", (user_id, state))
        conn.commit()
        conn.close()

    def get_user_state(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT state FROM user_state WHERE user_id = ? ORDER BY id DESC LIMIT 1", (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None

    def set_user_state(self, user_id, state):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_state (user_id, state) VALUES (?,?)", (user_id, state))
        conn.commit()
        conn.close()

    def clear_user_state(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_state WHERE user_id = ?", (user_id,))
        conn.commit()
        conn.close()

    def clear_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM user_state")
        cursor.execute("DELETE FROM user_selected_category")
        conn.commit()
        conn.close()

    def create_selected_category_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_selected_category (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def save_user_selected_category(self, user_id, category):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_selected_category (user_id, category) VALUES (?, ?)", (user_id, category))
        conn.commit()
        conn.close()

    def get_user_selected_category(self, user_id):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT category FROM user_selected_category WHERE user_id = ? ORDER BY id DESC LIMIT 1",
                       (user_id,))
        result = cursor.fetchone()
        conn.close()
        if result is not None:
            return result[0]
        else:
            return None
