from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def start_button():
    key_board = ReplyKeyboardMarkup(
        resize_keyboard=True)

    button_one = KeyboardButton('/Отель')
    button_two = KeyboardButton('/Посмотреть кафе и рестораны')
    button_three = KeyboardButton('/Погода')

    key_board.add(button_one )
    key_board.add(button_two)
    key_board.add(button_three)
    return key_board
