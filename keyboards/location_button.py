from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def location_button():
    """
    Функция для создания и возврата клавиши запроса геопозиции.

    Действие:
        Создает и возвращает клавишу для запроса геопозиции.
        Клавиша "Поделиться геопозицией 🗺️" использует request_location=True для запроса геолокации.

    Возвращает:
        ReplyKeyboardMarkup: Объект клавиатуры с единственной кнопкой запроса геопозиции.
    """
    button_one = KeyboardButton('Поделиться геопозицией 🗺️', request_location=True)
    location_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    location_keyboard.add(button_one)
    return location_keyboard
