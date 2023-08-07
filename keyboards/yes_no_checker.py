from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def yes_no_checker():
    """
    Функция для создания инлайн-клавиатуры с двумя кнопками: "Ввести даты заново" и "Продолжить".

    Действие:
        Создает и возвращает инлайн-клавиатуру с двумя кнопками.
        Первая кнопка предлагает пользователю ввести даты заново.
        Вторая кнопка предлагает пользователю продолжить без изменений.

    Возвращает:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками "Ввести даты заново" и "Продолжить".
    """
    yes_no_keyboard = InlineKeyboardMarkup(row_width=1)
    yes_no_keyboard.add(InlineKeyboardButton(text='Ввести даты заново', callback_data='//да'))
    yes_no_keyboard.add(InlineKeyboardButton(text='Продолжить', callback_data='//нет'))
    return yes_no_keyboard
