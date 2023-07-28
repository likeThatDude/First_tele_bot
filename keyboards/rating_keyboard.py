from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def rating_button():
    rating_key = InlineKeyboardMarkup(row_width=1)
    rating_key.add(InlineKeyboardButton(text='С высокого', callback_data='//больше'))
    rating_key.add(InlineKeyboardButton(text='С низкого', callback_data='//меньше'))
    return rating_key
