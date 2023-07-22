from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button_one = KeyboardButton('/Подобрать отель')
button_two = KeyboardButton('/Посмотреть кафе и рестораны')
button_three = KeyboardButton('/Погода')
button_four = KeyboardButton('Поделиться контактом ☎️', request_contact=True)  # второй аргумент - передать телефон
button_five = KeyboardButton('Поделиться геопозицией 🗺️', request_location=True)  # второй аргумент это передать локацию

key_board = ReplyKeyboardMarkup(
    resize_keyboard=True)  # one_time_keyboard=True Клавиатура будет опускаться после нажатия

key_board.add(button_one)  # .add Добавление по одной кнопки
key_board.add(button_two)
key_board.insert(button_three)  # .insert Добавляет кнопки в ряд, пока есть место
