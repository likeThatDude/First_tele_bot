from geopy import Nominatim
from create_bot import bot


async def user_location(message):
    """
    Получает название города из сообщения пользователя, содержащего либо геолокацию, либо текстовый ввод.

    Параметры:
       message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.

    Возвращает:
       str or None: Название города, если удалось получить из геолокации или текстового ввода, или None, если не удалось определить.

    Действие:
       Если сообщение пользователя содержит геолокацию, использует функцию get_city_name для определения названия города
       по заданным координатам широты и долготы. Если название города не определено, отправляет сообщение пользователю
       с просьбой прислать геолокацию ещё раз или ввести город вручную.

       Если сообщение пользователя не содержит геолокацию, считает текстовый ввод названия города
       и возвращает его, приведенным к нижнему регистру.

       Если название города не определено и сообщение не содержит текстового ввода,
       возвращает None, чтобы обработка названия города выполнялась в вызывающей функции.
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
    Получает название города по заданным координатам широты и долготы.

    Параметры:
        latitude (float): Широта местоположения.
        longitude (float): Долгота местоположения.

    Возвращает:
        str or None: Название города, если удалось определить, или None, если название не найдено.

    Действие:
        Использует геокодер Nominatim для определения названия города по заданным координатам.
        Для определения города используется обратное геокодирование (reverse geocoding).
        Возвращает название города, если оно найдено, или None, если название города не определено или произошла ошибка.
    """

    geolocator = Nominatim(user_agent="tele_bot")
    location = geolocator.reverse((latitude, longitude), language="ru")

    if location and location.raw.get("address"):
        city = location.raw["address"].get("city")
        if city:
            return city
    return None
