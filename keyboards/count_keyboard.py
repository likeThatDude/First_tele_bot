from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_count():
    """
    Функция, возвращающая InlineKeyboardMarkup с кнопками для выбора количества отелей.

    Returns:
        InlineKeyboardMarkup: Объект с кнопками выбора числа.
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('3', callback_data='//3'))
    keyboard.add(InlineKeyboardButton('7', callback_data='//7'))
    keyboard.add(InlineKeyboardButton('10', callback_data='//10'))
    keyboard.add(InlineKeyboardButton('30', callback_data='//30'))

    return keyboard
