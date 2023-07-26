from create_bot import hotel_key
import requests


async def get_hotel_photo(hotel_id):
    url = "https://booking-com.p.rapidapi.com/v1/hotels/photos"

    querystring = {"hotel_id": hotel_id, "locale": "ru"}

    headers = {
        "X-RapidAPI-Key": hotel_key,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    photo_list = []
    response = requests.get(url, headers=headers, params=querystring)
    response = response.json()
    for i in response[:5]:
        photo_list.append(i['url_max'])
    return photo_list
