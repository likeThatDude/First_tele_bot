from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_one = KeyboardButton('Поделиться геопозицией 🗺️', request_location=True)

location_button = ReplyKeyboardMarkup(resize_keyboard=True)

location_button.add(button_one)
