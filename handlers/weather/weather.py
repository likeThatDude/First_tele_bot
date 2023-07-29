import json
import datetime
from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.location_button import location_button
from keyboards.start_keyboard import start_button
from utilities.find_location.find_city import user_location
from utilities.weather.get_weather import location_weather


class FSMWeather(StatesGroup):
    correct_cite_name = State()


async def get_city(message: types.Message):
    """
    Функция, которая запускается при команде "/Погода" или начале запроса погоды.
    Она запрашивает у пользователя название города или просит поделиться геолокацией для получения данных о погоде.

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.

    Возвращает:
        None

    Действие:
        Отправляет сообщение пользователю с текстом о запросе названия города или поделиться местоположением.
        В сообщении будет также прикреплена пользовательская клавиатура с кнопкой "Отправить местоположение".
        Задает состояние FSMWeather.correct_cite_name для следующего шага конечного автомата.
    """
    location_keyboard = await location_button()
    await bot.send_message(message.from_user.id, '\t\t⛅️    Меню погоды    ⛅️\n'
                                                 '\nДля начала мне нужно знать город,'
                                                 '\nв котором вам нужно узнать погоду.'
                                                 '\nВведите город или поделитесь геолокацией со мной.'
                                                 '\nЧтобы поделиться, нажмите кнопку снизу.',
                           reply_markup=location_keyboard)
    await FSMWeather.correct_cite_name.set()


async def get_weather(message: types.Message, state: FSMContext):
    """
    Функция, которая вызывается после того, как пользователь предоставил название города или поделился геолокацией.
    Она получает данные о погоде для указанного города с использованием API OpenWeatherMap
    и отправляет результат пользователю.

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.
        state (FSMContext): Контекст состояния конечного автомата для управления диалогом с пользователем.

    Выходные параметры: нет.

    Действие:
        Получает название города из пользовательского ввода или местоположения с помощью функции user_location.
        Использует полученное название города для получения данных о погоде с помощью функции location_weather.
        Если запрос выполнен успешно (статус 200), отправляет пользователю сообщение с информацией о погоде,
        включая температуру, ощущаемую температуру, описание погоды и влажность.
        Завершает состояние конечного автомата. Если название города недействительно,
        отправляет пользователю сообщение об ошибке с просьбой повторить ввод.
    """

    current_date_time = datetime.datetime.now()
    formatted_date_time = current_date_time.strftime('%d/%m/%Y %H:%M:%S')
    city_name = await user_location(message=message)

    all_data = await location_weather(city_name=city_name)

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
        await bot.send_message(message.from_user.id, 'Для продолжения работы выберите один из пунктов меню',
                               reply_markup=start_button)
    else:
        await bot.send_message(message.from_user.id, 'Ошибка ввода города. Пожалуйста, попробуйте еще раз.')


def register_handler_weather(dp: Dispatcher):
    """
    Функция для регистрации обработчиков сообщений связанных с запросами погоды.

    Входные параметры:
    - dp: объект типа Dispatcher - диспетчер, который управляет обработкой сообщений.

    Выходные параметры: нет.
    Действие:
        Регистрирует функции get_city и get_weather как обработчики для бота.
        get_city будет вызываться при получении команды "/Погода".
        get_weather будет вызываться при получении текстовых сообщений или местоположения,
        когда пользователь находится в состоянии FSMWeather.correct_cite_name.
    """
    dp.register_message_handler(get_city, commands=['Погода'], state=None)
    dp.register_message_handler(get_weather, content_types=['text', 'location'], state=FSMWeather.correct_cite_name)
