import aiohttp
from create_bot import rest_key



async def get_city_id(city_name):
    """
    Функция для получения идентификатора города по его имени с использованием API.

    Параметры:
        city_name (str): Название города для поиска и получения идентификатора.

    Возвращает:
        id города, если успешно найден, либо False в случае ошибки.
    """
    url = "https://worldwide-restaurants.p.rapidapi.com/typeahead"

    payload = {
        "q": city_name,
        "language": "ru_RU"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": rest_key,
        "X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            if response.status == 200:
                response_data = await response.json()
                location_id = response_data['results']['data'][0]['result_object']['location_id']
                return location_id
            else:
                return False
