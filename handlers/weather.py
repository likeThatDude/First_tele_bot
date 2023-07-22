from create_bot import bot, weather_key
from aiogram import types, Dispatcher
import requests
import json
import datetime
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.weather_buttom import location_button
from geopy import Nominatim


class FSMWeather(StatesGroup):
    correct_cite_name = State()


async def get_city(message: types.Message):
    """
    Функция, которая запускается при команде "/Погода" или начале запроса погоды.
    Она запрашивает у пользователя название города или просит поделиться геолокацией для получения данных о погоде.

    Входные параметры:
    - message: объект типа types.Message - сообщение от пользователя.

    Выходные параметры: нет.
    """
    await bot.send_message(message.from_user.id, '\t\t⛅️    Меню погоды    ⛅️\n'
                                                 '\nДля начала мне нужно знать город,'
                                                 '\nв котором вам нужно узнать погоду.'
                                                 '\nВведите город или поделитесь геолокацией со мной.'
                                                 '\nЧтобы поделиться, нажмите кнопку снизу.',
                           reply_markup=location_button)
    await FSMWeather.correct_cite_name.set()


async def get_weather(message: types.Message, state: FSMContext):
    """
    Функция, которая вызывается после того, как пользователь предоставил название города или поделился геолокацией.
    Она получает данные о погоде для указанного города с использованием API OpenWeatherMap
    и отправляет результат пользователю.

    Входные параметры:
    - message: объект типа types.Message - сообщение от пользователя.
    - state: объект типа FSMContext - состояние бота для управления его поведением.

    Выходные параметры: нет.
    """
    current_date_time = datetime.datetime.now()
    formatted_date_time = current_date_time.strftime('%d/%m/%Y %H:%M:%S')
    if message.location:
        city_name = await get_city_name(message['location']['latitude'], message['location']['longitude'])
        if city_name is None:
            await bot.send_message(message.from_user.id, 'Извините, я не смог найти ваш город.'
                                                         '\nПопробуйте прислать геолокацию ещё раз '
                                                         '\nили напишите город вручную')
    else:
        city_name = message.text.strip().lower()
    all_data = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_key}&units=metric&lang=ru')

    if all_data.status_code == 200:
        data = json.loads(all_data.text)
        await bot.send_message(message.from_user.id, f'Погода в городе: {city_name.capitalize()}\n'
                                                     f'\nДанные на: {formatted_date_time}\n'
                                                     f'\nТемпература: {round(data["main"]["temp"], 1)} °C'
                                                     f'\nОщущается как: {round(data["main"]["feels_like"], 1)} °C'
                                                     f'\nСейчас на улице: '
                                                     f'{data["weather"][0]["description"].capitalize()}'
                                                     f'\nВлажность: {round(data["main"]["humidity"], 1)}%')
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, 'Ошибка ввода города. Пожалуйста, попробуйте еще раз.')


async def get_city_name(latitude, longitude):
    """
    Функция для получения названия города по переданным координатам геолокации.

    Входные параметры:
    - latitude: широта геолокации.
    - longitude: долгота геолокации.

    Выходные параметры:
    - city: название города, если удалось определить, иначе None.
    """
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse((latitude, longitude), language="ru")

    if location and location.raw.get("address"):
        city = location.raw["address"].get("city")
        if city:
            return city
    return None


def register_handler_weather(dp: Dispatcher):
    """
    Функция для регистрации обработчиков сообщений связанных с запросами погоды.

    Входные параметры:
    - dp: объект типа Dispatcher - диспетчер, который управляет обработкой сообщений.

    Выходные параметры: нет.
    """
    dp.register_message_handler(get_city, commands=['Погода'], state=None)
    dp.register_message_handler(get_weather, content_types=['text', 'location'], state=FSMWeather.correct_cite_name)
