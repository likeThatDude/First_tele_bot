from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def yes_no_checker():
    yes_no_keyboard = InlineKeyboardMarkup(row_width=1)
    yes_no_keyboard.add(InlineKeyboardButton(text='Да', callback_data='//да'))
    yes_no_keyboard.add(InlineKeyboardButton(text='Нет', callback_data='//нет'))
    return yes_no_keyboard
