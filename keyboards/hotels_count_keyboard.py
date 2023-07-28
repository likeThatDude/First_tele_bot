from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_count():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('5', callback_data='//5'))
    keyboard.add(InlineKeyboardButton('8', callback_data='//10'))
    keyboard.add(InlineKeyboardButton('10', callback_data='//15'))
    keyboard.add(InlineKeyboardButton('20', callback_data='//20'))
    keyboard.add(InlineKeyboardButton('30', callback_data='//30'))
    return keyboard
