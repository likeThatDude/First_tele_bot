from geopy import Nominatim
from create_bot import bot


async def user_location(message):
    """
    Функция для определения местоположения пользователя на основе сообщения.

    Аргументы:
        message (telegram.Message): Объект сообщения пользователя, который может содержать геолокацию
        или текстовое представление города.

    Возвращает:
        str: Имя города, определенное на основе геолокации или текстового представления.

    Примечание:
        Функция асинхронная (async), предназначена для работы в асинхронном окружении .
        Если в сообщении найдена геолокация, функция попытается получить имя города на основе координат
        с помощью внешней функции "get_city_name".
        Если имя города не найдено или сообщение не содержит геолокацию, будет использован текстовый ввод пользователя.
    """
    if message.location:
        city_name = await get_city_name(message['location']['latitude'], message['location']['longitude'])
        if city_name is None:
            await bot.send_message(message.from_user.id, 'Извините, я не смог найти ваш город.'
                                                         '\nПопробуйте прислать геолокацию ещё раз '
                                                         '\nили напишите город вручную')
    else:
        city_name = message.text.strip().lower()
    return city_name


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
        print(city)
        if city:
            return city
    return None
