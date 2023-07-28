from create_bot import hotel_key
import aiohttp


async def get_hotel_photo(hotel_id):
    url = "https://booking-com.p.rapidapi.com/v1/hotels/photos"

    querystring = {"hotel_id": hotel_id, "locale": "ru"}

    headers = {
        "X-RapidAPI-Key": hotel_key,
        "X-RapidAPI-Host": "booking-com.p.rapidapi.com"
    }

    photo_list = []
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, params=querystring) as response:
            response_data = await response.json()
            for i in response_data[:5]:
                photo_list.append(i['url_max'])
    return photo_list
