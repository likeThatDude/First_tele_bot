import aiohttp

from create_bot import hotel_key


async def get_hotel_photo(hotel_id):
    """
    Получает список фотографий отеля с помощью Booking.com API.

    Параметры:
        hotel_id (str): Идентификатор отеля, для которого нужно получить фотографии.

    Возвращает:
        photo_list (list): Список URL-адресов фотографий отеля. Максимум 5 фотографий.

    Исключения:
        Если возникают проблемы с соединением или запросом к API, может быть возбуждено исключение aiohttp.ClientError.

    Примечание:
        Для успешного выполнения запроса требуется наличие действительного ключа доступа (API key) к Booking.com API.
        Перед использованием функции убедитесь, что вы предоставили корректный ключ доступа (API key) в файле create_bot.py
        через переменную hotel_key.
    """
    url = "https://booking-com.p.rapidapi.com/v1/hotels/photos"

    querystring = {"hotel_id": hotel_id, "locale": "ru"}

    headers = {
        "X-RapidAPI-Key": hotel_key,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com",
    }

    photo_list = []
    async with aiohttp.ClientSession() as session:
        async with session.get(
            url, headers=headers, params=querystring
        ) as response:
            response_data = await response.json()
            for i in response_data[:5]:
                photo_list.append(i["url_max"])
    return photo_list
