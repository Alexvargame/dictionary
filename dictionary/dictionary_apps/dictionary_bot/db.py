import sqlite3
from decimal import Decimal
from datetime import datetime, timedelta, date
import sqlite3

class BotDBClass:
    def __init__(self, db_file):
        print('DBFILE', db_file)
        self.file = db_file

    def user_exists(self, user_bot_id):
        print('botid', user_bot_id)
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        result = cursor.execute(
            'SELECT user_bot_id FROM users_baseuser WHERE chat_id=?',
            (user_bot_id,)
        ).fetchall()
        conn.close()
        return bool(len(result))

    def get_username_user(self, user_bot_id):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        result = cursor.execute(
            'SELECT username FROM users_baseuser WHERE chat_id=?',
            (user_bot_id,)
        ).fetchone()[0]
        conn.close()
        return result

    def get_user_id(self, user_bot_id):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        result = cursor.execute(
            'SELECT id FROM users_baseuser WHERE chat_id=?',
            (user_bot_id,)
        ).fetchone()[0]
        conn.close()
        return result

    def get_user(self, user_bot_id):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        result = cursor.execute(
            'SELECT * FROM users_baseuser WHERE chat_id=?',
            (user_bot_id,)
        ).fetchone()[0]
        conn.close()
        return result

    def get_user_profile(self, user_id):
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        result = cursor.execute(
            'SELECT * FROM users_baseuser WHERE id=?',
            (user_id,)
        ).fetchone()
        conn.close()
        return result

# class BotDBClass:
#
#     def __init__(self, db_file):
#         print('DBFILE', db_file)
#         self.file = db_file
#         self.conn = sqlite3.connect(db_file, check_same_thread=False)
#         self.cursor = self.conn.cursor()
#
#     def user_exists(self, user_bot_id):
#         print('botid', user_bot_id)
#         result = self.cursor.execute(
#             'select user_bot_id from users_baseuser where chat_id=?',
#             (user_bot_id,)).fetchall()
#         return bool(len(result))
#
#     def get_username_user(self, user_bot_id):
#         return self.cursor.execute('select username from users_baseuser where chat_id=?', (user_bot_id,)).fetchone()[0]
#
#     def get_user_id(self, user_bot_id):
#         return self.cursor.execute('select id from users_baseuser where chat_id=?', (user_bot_id,)).fetchone()[0]
#     def get_user(self, user_bot_id):
#         return self.cursor.execute('select * from users_baseuser where chat_id=?',
#                                    (user_bot_id,)).fetchone()[0]
#
#     def get_user_profile(self, user_id):
#         return self.cursor.execute('select * from users_baseuser where id=?',(user_id,)).fetchone()
#
#     def close(self):
#         self.conn.close()
#
#
