from create_bot import hotel_key
import aiohttp


async def create_hotels_dict(city_id, checkin_date, checkout_date, rating, hotels_count, order_by, adults_number=1):
    """
    Создает словарь отелей с их оценками в указанном городе.

    Аргументы:
        city_id (int): ID города, в котором будет производиться поиск отелей.
        checkin_date (str): Дата заезда в формате "ГГГГ-ММ-ДД".
        checkout_date (str): Дата выезда в формате "ГГГГ-ММ-ДД".
        rating (bool): Определяет, как будут сортироваться отели по оценки.
            Если True, отели будут отсортированы по убыванию оценки.
            Если False, отели будут отсортированы по возрастанию оценки.
        hotels_count (int): Количество отелей с оценками, которые нужно получить.
        order_by (str): Синхронен с rating, если rating is True то выводит отели с большим количеством звёзд и наоборот
        adults_number (int, optional): Количество взрослых, проживающих в номере. По умолчанию 1.

    Возвращает:
        list: Список отелей с оценками, отсортированный по оценке, 'rating' может быть True либо False,
        для корректной работы reverse=rating.

    Примечание:
        Данная функция использует API Booking.com для получения данных об отелях.

    Пример:
        hotels = await create_hotels_dict(city_id=12345, checkin_date="2023-08-01", checkout_date="2023-08-10",
                                          rating=True, hotels_count=10, adults_number=2)
    """
    hotels_with_rating = []
    page_number = 0
    while True:
        if page_number == 5:
            break
        querystring = {
            "checkin_date": checkin_date,
            "dest_type": "city",
            "units": "metric",
            "checkout_date": checkout_date,
            "adults_number": adults_number,
            "order_by": order_by,
            "dest_id": city_id,
            "filter_by_currency": "USD",
            "locale": "ru",
            "room_number": "1",
            "children_number": "1",
            "children_ages": "5,0",
            "categories_filter_ids": "class::2,class::4,free_cancellation::1",
            "page_number": page_number,
            "include_adjacency": "true"
        }

        url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

        headers = {
            "X-RapidAPI-Key": hotel_key,
            "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                response_data = await response.json()
                if "result" in response_data:
                    for hotel_data in response_data["result"]:
                        if not hotel_data['review_score'] is None and isinstance(hotel_data['review_score'],
                                                                                 (float, int)):
                            hotels_with_rating.append(hotel_data)
                            if len(hotels_with_rating) == hotels_count:
                                break
                    else:
                        page_number += 1
                        continue
                    break

    return sorted(hotels_with_rating, key=lambda x: x['review_score'], reverse=rating)
