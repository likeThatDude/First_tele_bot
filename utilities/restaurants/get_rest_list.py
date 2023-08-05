import aiohttp
from create_bot import rest_key

async def get_rest_list(location_id, list_size):
    url = "https://worldwide-restaurants.p.rapidapi.com/search"

    payload = {
        "language": "ru_RU",
        "limit": list_size,
        "location_id": location_id,
        "currency": "USD"
    }
    headers = {
        "content-type": "application/x-www-form-urlencoded",
        "X-RapidAPI-Key": rest_key,
        "X-RapidAPI-Host": "worldwide-restaurants.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=payload, headers=headers) as response:
            response = await response.json()
            print(response)
            result_list = response['results']['data']
            return result_list
