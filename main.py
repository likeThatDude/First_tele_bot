from aiogram.utils import executor
from handlers import start
from handlers.weather import weather
from handlers.hotels import hotels
from handlers.restaurants import  restaurants
from handlers.search_history import history
from create_bot import dp
from data_base import sqlite_db


async def on_startup(_):
    """
    Функция, вызываемая при запуске бота.

    Параметры:
        _ (Any): Дополнительный параметр (не используется).

    Действие:
        Выводит сообщение о том, что бот онлайн.
    """
    print('Bot online !')
    sqlite_db.sql_start()

start.register_handler_start(dp)
weather.register_handler_weather(dp)
hotels.register_handler_hotels(dp)
restaurants.register_handler_hotels(dp)
history.register_handler_hotels(dp)

if __name__ == '__main__':
    """
    Точка входа в программу.

    Действие:
        Запускает бота для прослушивания обновлений.
    """
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
