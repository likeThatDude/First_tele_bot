from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cities_button_generator(dict_with_result):
    cities_keyboard = InlineKeyboardMarkup(row_width=1)
    for city in dict_with_result:
        cities_keyboard.add(InlineKeyboardButton(text=f'{dict_with_result[city]["label"]}',
                                                 callback_data=f'city: {city}'))
    return cities_keyboard
