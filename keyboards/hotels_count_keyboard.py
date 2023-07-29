from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_count():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('3', callback_data='//3'))
    keyboard.add(InlineKeyboardButton('7', callback_data='//7'))
    keyboard.add(InlineKeyboardButton('10', callback_data='//10'))
    return keyboard
