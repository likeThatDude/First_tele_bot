from aiogram import types, Dispatcher
from create_bot import bot
from keyboards.start_keyboard import key_board
from datetime import datetime


async def start_command(message: types.Message):
    current_time = datetime.now().time()
    hour = current_time.hour

    if 5 <= hour < 10:
        time_period = "Доброе утро"
    elif 10 <= hour < 17:
        time_period = "Добрый день"
    elif 17 <= hour < 20:
        time_period = "Добрый вечер"
    else:
        time_period = "Доброй ночь"

    await bot.send_message(message.from_user.id, f'{time_period}, {message.from_user.first_name} !\n'
                                                 f'\nЯ бот помощник, у меня есть следующие функции: '
                                                 f'\n1) Поиск отелей. 🏨'
                                                 f'\n2) Поиск ресторанов, кафе.🍜'
                                                 f'\n3) Могу узнать погоду в интересующем вас городе.🌦',
                           reply_markup=key_board)


def register_handler_start(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
