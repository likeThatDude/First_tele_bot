from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def rating_button():
    """
    Функция для создания и возврата инлайн-клавиатуры с кнопками для выбора сортировки по рейтингу.

    Действие:
        Создает и возвращает инлайн-клавиатуру с кнопками для выбора сортировки по рейтингу.
        Каждая кнопка предоставляет опцию для сортировки ресторанов по рейтингу.

    Возвращает:
        InlineKeyboardMarkup: Объект инлайн-клавиатуры с кнопками для выбора сортировки по рейтингу.
    """
    rating_key = InlineKeyboardMarkup(row_width=1)
    rating_key.add(
        InlineKeyboardButton(text="С высокого", callback_data="//больше")
    )
    rating_key.add(
        InlineKeyboardButton(text="С низкого", callback_data="//меньше")
    )
    return rating_key
