import aiohttp

from create_bot import hotel_key


async def get_dic_with_cities(city):
    """
    Получает информацию о городе из API Booking.com.

    Функция отправляет асинхронный HTTP-запрос (GET) к API Booking.com для получения информации о заданном городе.
    В качестве аргумента, функция принимает название города, по которому будет выполнен запрос.

    Параметры:
        city (str): Название города для выполнения запроса к API.

    Возвращает:
        dict: Словарь с данными, полученными от API Booking.com. Данные содержат информацию о городе,
        его расположении и другие сведения, связанные с отелями.

    Пример:
        city_info = await get_dic_with_cities("Москва")
        print(city_info)
        # Примерный вывод:
        # {
        #     "city_name": "Москва",
        #     "city_id": "4355",
        #     "country": "Россия",
        #     "country_code": "RU",
        #     "latitude": "55.751244",
        #     "longitude": "37.618423",
        #     "number_of_hotels": 2352,
        #     ...
        # }

    Примечание:
        - Для использования функции требуется наличие и корректность API-ключа Booking.com,
          который должен быть предварительно задан в переменной `hotel_key`.
        - Функция использует библиотеку `aiohttp` для асинхронного выполнения HTTP-запросов.
    """
    url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
    headers = {
        "X-RapidAPI-Key": hotel_key,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
    }

    querystring = {"name": city, "locale": "ru"}
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, headers=headers, params=querystring
        ) as response:
            data = await response.json()
            return data
