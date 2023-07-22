from aiogram.utils import executor

from handlers import start, weather
from create_bot import dp


async def on_startup(_):
    print('Bot online !')

start.register_handler_start(dp)
weather.register_handler_weather(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
