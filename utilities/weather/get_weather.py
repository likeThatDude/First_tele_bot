import requests
from create_bot import weather_key


async def location_weather(city_name):
    """
    Получает данные о погоде для указанного города с помощью API OpenWeatherMap.

    Параметры:
        city_name (str): Название города, для которого запрашивается информация о погоде.

    Возвращает:
        requests.Response: Объект Response, содержащий данные о погоде.

    Действие:
        Выполняет запрос к API OpenWeatherMap, используя указанное название города и ключ API (weather_key).
        Запрашивает данные в метрической системе (температура в градусах Цельсия) и на русском языке.
        Возвращает объект Response с данными о погоде. Дополнительная обработка данных должна выполняться в вызывающей функции.
    """

    weather_data = requests.get(
        f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={weather_key}&units=metric&lang=ru')

    return weather_data
