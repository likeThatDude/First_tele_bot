from aiogram.utils import executor
from handlers import start
from handlers.weather import weather
from handlers.hotels import hotels
from create_bot import dp


async def on_startup(_):
    print('Bot online !')

start.register_handler_start(dp)
weather.register_handler_weather(dp)
hotels.register_handler_hotels(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
