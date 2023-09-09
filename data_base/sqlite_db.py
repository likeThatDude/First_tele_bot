import sqlite3 as sq
from datetime import datetime
import pytz

def sql_start():
    global base, cur
    base = sq.connect('bot_database.db')
    cur = base.cursor()
    if base:
        print('Database connected!')
    base.execute('CREATE TABLE IF NOT EXISTS users('
                 'user_tg_id INT UNIQUE, '
                 'user_name TEXT, '
                 'creation_date TIME'
                 ')')
    base.execute('CREATE TABLE IF NOT EXISTS request_history('
                 'user_id INT, '
                 'category TEXT, '
                 'request TEXT, '
                 'request_date TIME'
                 ')')

    cur.execute('CREATE INDEX IF NOT EXISTS idx_user_tg_id ON users(user_tg_id)')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_user_id ON request_history(user_id)')

    base.commit()


async def add_user(user_tg_id, user_name):
    current_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT OR IGNORE INTO users  VALUES (?, ?, ?)', (user_tg_id, user_name, current_time))
    base.commit()


async def add_request(data):
    current_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO request_history VALUES (?, ?, ?, ?)', (*data, current_time))
    base.commit()
