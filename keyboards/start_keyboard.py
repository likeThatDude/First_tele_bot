from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def start_button():
    """
    Функция для создания и возврата клавиатуры с кнопками для начала различных операций.

    Действие:
        Создает и возвращает клавиатуру с кнопками для начала различных операций, таких как "Отель", "Рестораны" и "Погода".

    Возвращает:
        ReplyKeyboardMarkup: Объект клавиатуры с кнопками для начала различных операций.
    """
    key_board = ReplyKeyboardMarkup(
        resize_keyboard=True)

    key_board.add(KeyboardButton('/Отель')).add(KeyboardButton('/Рестораны')).add(
        KeyboardButton('/Погода'))
    return key_board
