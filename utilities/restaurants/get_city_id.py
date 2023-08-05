import aiohttp
from create_bot import rest_key



async def get_city_id(city_name):
    url = "https://worldwide-restaurants.p.rapidapi.com/typeahead"

    payload = {
        "q": city_name,
        "language": "ru_RU"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": rest_key,
        "X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            response_data = await response.json()
            print('id')
            print(response_data)
            location_id = response_data['results']['data'][0]['result_object']['location_id']
            return location_id

