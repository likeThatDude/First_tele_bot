import json
import requests
from create_bot import hotel_key

url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
headers = {
    "X-RapidAPI-Key": hotel_key,
    "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
}


async def get_dic_with_cities(city):
    querystring = {"name": city, "locale": "ru"}
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    return data
