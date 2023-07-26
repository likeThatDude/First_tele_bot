from create_bot import hotel_key
import requests


async def create_hotels_dict(city_id, checkin_date, checkout_date, page_number=0, adults_number=1):
    querystring = {"checkin_date": checkin_date, "dest_type": "city", "units": "metric", "checkout_date": checkout_date,
                   "adults_number": adults_number, "order_by": "popularity", "dest_id": city_id,
                   "filter_by_currency": "USD",
                   "locale": "ru", "room_number": "1", "children_number": "2", "children_ages": "5,0",
                   "categories_filter_ids": "class::2,class::4,free_cancellation::1", "page_number": page_number,
                   "include_adjacency": "true"
                   }

    url = "https://booking-com.p.rapidapi.com/v1/hotels/search"

    headers = {"X-RapidAPI-Key": hotel_key,
               "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
               }

    response = requests.get(url, headers=headers, params=querystring)
    response_data = response.json()
    return response_data['result']
