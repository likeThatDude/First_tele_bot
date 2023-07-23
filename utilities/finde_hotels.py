from create_bot import hotel_key
import requests


async def create_hotels_dict(city_id, checkin_date, checkout_date):
    querystring = {"order_by": "popularity",
                   "adults_number": "2",
                   "checkin_date": checkin_date,
                   "filter_by_currency": "USD",
                   "dest_id": city_id,
                   "locale": "ru",
                   "checkout_date": checkout_date,
                   "units": "metric",
                   "room_number": "1",
                   "dest_type": "city",
                   "include_adjacency": "true",
                   "children_number": "1",
                   "page_number": "1",
                   "children_ages": "5,0",
                   "categories_filter_ids": "class::2,class::4,free_cancellation::1"
                   }

    url = "https://booking-com.p.rapidapi.com/v2/hotels/search"

    headers = {"X-RapidAPI-Key": hotel_key,
               "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
               }

    response = requests.get(url, headers=headers, params=querystring)

    print(response.json())
