import sqlite3 as sq
from datetime import datetime
import pytz


def sql_start():
    """
    Функция для инициализации и подключения к базе данных SQLite.

    Параметры: нет.

    Действие:
        - Устанавливает соединение с базой данных.
        - Создает таблицу 'users' для хранения информации о пользователях, если она не существует.
        - Создает таблицу 'request_history' для хранения истории запросов, если она не существует.
        - Создает индексы для ускорения поиска данных.
    """
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
    """
    Функция для добавления пользователя в базу данных.

    Параметры:
        user_tg_id (int): Идентификатор Telegram пользователя.
        user_name (str): Имя пользователя.

    Действие:
        Добавляет пользователя в таблицу 'users' с указанными данными.
    """
    current_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT OR IGNORE INTO users  VALUES (?, ?, ?)', (user_tg_id, user_name, current_time))
    base.commit()


async def add_request(data):
    """
    Функция для добавления запроса в историю запросов.

    Параметры:
        data (tuple): Кортеж данных о запросе, содержащий (user_id, category, request).

    Действие:
        Добавляет информацию о запросе в таблицу 'request_history'.
    """
    current_time = datetime.now(pytz.timezone('Europe/Moscow')).strftime('%Y-%m-%d %H:%M:%S')
    cur.execute('INSERT INTO request_history VALUES (?, ?, ?, ?)', (*data, current_time))
    base.commit()


async def get_history(user_id):
    """
    Функция для получения истории запросов пользователя.

    Параметры:
        user_id (int): Идентификатор Telegram пользователя.

    Возвращает:
        list: Список кортежей с данными о запросах пользователя.

    Действие:
        Извлекает последние 10 запросов пользователя из таблицы 'request_history'.
    """
    cur.execute("""
                SELECT 
                    request_history.category, 
                    request_history.request, 
                    request_history.request_date
                FROM 
                    request_history
                JOIN 
                    users
                ON 
                    request_history.user_id = users.user_tg_id
                WHERE
                    users.user_tg_id = ?
                ORDER BY 
                    request_history.request_date DESC
                LIMIT  10
                """, (user_id,))
    user_search_data = cur.fetchall()
    return user_search_data