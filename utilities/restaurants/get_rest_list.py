import aiohttp
from create_bot import rest_key

async def get_rest_list(location_id):
    """
    Функция для получения списка ресторанов для заданного идентификатора местоположения.

    Параметры:
        location_id (int): Идентификатор местоположения (города).
        list_size (int): Количество ресторанов для получения.

    Возвращает:
        Список словарей с информацией о ресторанах,
        если успешно получен, либо False в случае ошибки.
    """
    url = "https://worldwide-restaurants.p.rapidapi.com/search"

    payload = {
        "language": "ru_RU",
        "location_id": location_id,
        "currency": "USD",
        "offset": "0"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": rest_key,
        "X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            if response.status == 200:
                response = await response.json()
                result_list = response['results']['data']
                for i in result_list:
                    print(i)
                return result_list
            else:
                return False
