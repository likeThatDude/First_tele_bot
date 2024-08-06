from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def cities_button_generator(dict_with_result):
    """
    Генерирует встроенную клавиатуру с кнопками для каждого города из входного словаря.

    Параметры:
        dict_with_result: dict
            Словарь, содержащий данные о городах.
            Ключи представляют названия городов, а значения - словари с данными о каждом городе.

    Возвращает:
        InlineKeyboardMarkup
            Встроенную клавиатуру с кнопками для каждого города.
            Каждая кнопка содержит текст из ключа "label"(у каждого города в словаре есть этот ключ)
            соответствующего города, и данные обратного вызова (callback_data) будут в формате `//<city_name>`,
            где <city_name> - название города с ограничением в 33 символа.
            (35 символов - 2 "//" символа которые я использую для отлова в register_callback_query_handler,
            это ограничение callback_data).
            Эти данные обратного вызова можно использовать для идентификации нажатой кнопки с городом.

    Пример:
        # Пример входных данных
        city_data = {
            "New York": {
                "label": "Нью-Йорк",
                "population": 8175133,
                "country": "США",
            },
            "Tokyo": {
                "label": "Токио",
                "population": 13942856,
                "country": "Япония",
            },
        }

        # Генерация встроенной клавиатуры
        search_result = await get_dic_with_cities(city_name), файл hotels.py строка 35.
    """
    cities_keyboard = InlineKeyboardMarkup(row_width=1)
    for city, city_data in dict_with_result.items():
        truncated_city_name = city[:33]
        cities_keyboard.add(
            InlineKeyboardButton(
                text=city_data["label"],
                callback_data=f"//{truncated_city_name}",
            )
        )
    return cities_keyboard
