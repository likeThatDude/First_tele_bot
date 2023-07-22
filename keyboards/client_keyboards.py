from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

button_one = KeyboardButton('/Подобрать отель')
button_two = KeyboardButton('/Посмотреть кафе и рестораны')
button_three = KeyboardButton('/Посмотреть погоду')

key_board = ReplyKeyboardMarkup(resize_keyboard=True)

key_board.add(button_one)
key_board.add(button_two)
key_board.add(button_three)

