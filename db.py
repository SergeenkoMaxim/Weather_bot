import sqlite3


class BotDB:

    def __init__(self):
        self.conn = sqlite3.connect('User.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

    def user_exist(self, telegram_id):
        result = self.cursor.execute("SELECT id FROM Users WHERE telegram_id = ?", (telegram_id,))
        print(result.fetchone())
        return result.fetchone()

    def get_user_id(self, telegram_id):
        result = self.cursor.execute('SELECT id FROM Users WHERE telegram_id = ?', (telegram_id,))
        return result.fetchone()[0]

    def add_user(self, telegram_id):
        self.cursor.execute("INSERT INTO 'Users' ('telegram_id') VALUES (?)", (telegram_id,))
        return self.conn.commit()

    def add_time(self, telegram_id, user_time):
        self.cursor.execute("UPDATE USERS SET time = ? WHERE telegram_id = ?", (user_time, telegram_id,))
        return self.conn.commit()

    def add_city(self, telegram_id, user_city):
        self.cursor.execute("UPDATE USERS SET city = ? WHERE telegram_id = ?", (user_city, telegram_id,))
        return self.conn.commit()

    def get_city(self, telegram_id):
        city = self.cursor.execute("SELECT city FROM Users WHERE telegram_id = ?", (telegram_id,))
        return city.fetchone()[0]

    def get_time(self, telegram_id):
        time = self.cursor.execute("SELECT time FROM Users WHERE telegram_id = ?", (telegram_id,))
        return time.fetchone()[0]

    def get_id_with_time(self, user_time):
        telegram_it = self.cursor.execute("SELECT telegram_id FROM users WHERE time = ?", (user_time,))
        return telegram_it.fetchone()[0]

    def close(self):
        self.conn.close()


BotDB = BotDB()