import aiohttp
from create_bot import hotel_key


async def get_dic_with_cities(city):
    url = "https://booking-com.p.rapidapi.com/v1/hotels/locations"
    headers = {
        "X-RapidAPI-Key": hotel_key,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    querystring = {"name": city, "locale": "ru"}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            data = await response.json()
            return data
