from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def location_button():
    button_one = KeyboardButton('Поделиться геопозицией 🗺️', request_location=True)
    location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    location_keyboard.add(button_one)
    return location_keyboard
