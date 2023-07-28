from create_bot import hotel_key
import aiohttp


async def create_hotels_dict(city_id, checkin_date, checkout_date, rating, hotels_count, adults_number=1):
    hotels_with_rating = []
    page_number = 0
    while True:
        if page_number == 5:
            break
        print(f'Номер страницы: {page_number}')
        print(f'Длина списка: {len(hotels_with_rating)}')
        querystring = {"checkin_date": checkin_date, "dest_type": "city", "units": "metric",
                       "checkout_date": checkout_date,
                       "adults_number": adults_number, "order_by": "price", "dest_id": city_id,
                       "filter_by_currency": "USD",
                       "locale": "ru", "room_number": "1", "children_number": "1", "children_ages": "5,0",
                       "categories_filter_ids": "class::2,class::4,free_cancellation::1", "page_number": page_number,
                       "include_adjacency": "true"
                       }

        url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

        headers = {"X-RapidAPI-Key": hotel_key,
                   "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
                   }

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                response_data = await response.json()
                if "result" in response_data:
                    for hotel_data in response_data["result"]:
                        print(hotel_data)
                        if not hotel_data['review_score'] is None and isinstance(hotel_data['review_score'], (float, int)):
                            hotels_with_rating.append(hotel_data)
                            if len(hotels_with_rating) == hotels_count:
                                break
                    else:
                        page_number += 1
                        continue
                    break
    return sorted(hotels_with_rating, key=lambda x: x['review_score'], reverse=rating)
