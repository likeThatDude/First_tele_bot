from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def start_button():
    """
    Функция, возвращающая ReplyKeyboardMarkup с кнопками для начала взаимодействия.

    Returns:
        ReplyKeyboardMarkup: Объект с кнопками для начала взаимодействия.
    """
    key_board = ReplyKeyboardMarkup(
        resize_keyboard=True)

    key_board.add(KeyboardButton('/Отель')).add(KeyboardButton('/Посмотреть кафе и рестораны')).add(
        KeyboardButton('/Погода'))
    return key_board
