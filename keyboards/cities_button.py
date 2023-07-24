from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def cities_button_generator(dict_with_result):
    cities_keyboard = InlineKeyboardMarkup(row_width=1)
    for city, city_data in dict_with_result.items():
        cities_keyboard.add(InlineKeyboardButton(text=city_data["label"],
                                                 callback_data=f'//{city[:33]}'))
    return cities_keyboard
