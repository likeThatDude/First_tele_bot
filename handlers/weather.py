from create_bot import bot, weather_key
from aiogram import types, Dispatcher
import requests
import json
import datetime


async def get_weather(message: types.Message):
    current_date_time = datetime.datetime.now()
    formatted_date_time = current_date_time.strftime('%d/%m/%Y %H:%M:%S')
    city_name = message.text.strip().lower()
    all_data = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_key}&units=metric&lang=ru')

    if all_data.status_code == 200:
        data = json.loads(all_data.text)
        await bot.send_message(message.from_user.id, f'Погода в городе: {city_name.capitalize()}\n'
                                                     f'\nДанные на: {formatted_date_time}\n'
                                                     f'\nТемпература: {round(data["main"]["temp"], 1)} °C'
                                                     f'\nОщущается как: {round(data["main"]["feels_like"], 1)} °C'
                                                     f'\nСейчас на улице: {data["weather"][0]["description"].capitalize()}'
                                                     f'\nВлажность: {round(data["main"]["humidity"], 1)}%')
    else:
        await bot.send_message(message.from_user.id, 'Ошибка ввода города. Пожалуйста, попробуйте еще раз.')


def register_handler_weather(dp: Dispatcher):
    dp.register_message_handler(get_weather, commands=['weather'])
