from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_count():
    """
    Функция для создания инлайн-клавиатуры с кнопками для выбора количества ресторанов.

    Действие:
        Создает и возвращает инлайн-клавиатуру с кнопками для выбора количества ресторанов.
        Каждая кнопка соответствует определенному количеству ресторанов.

    Возвращает:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками для выбора количества ресторанов.
    """
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton('3', callback_data='//3'))
    keyboard.add(InlineKeyboardButton('7', callback_data='//7'))
    keyboard.add(InlineKeyboardButton('10', callback_data='//10'))
    keyboard.add(InlineKeyboardButton('30', callback_data='//30'))

    return keyboard
