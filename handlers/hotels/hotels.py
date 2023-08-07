import asyncio
from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from keyboards.location_button import location_button
from keyboards.cities_button import cities_button_generator
from keyboards.yes_no_checker import yes_no_checker
from keyboards.rating_keyboard import rating_button
from keyboards.start_keyboard import start_button
from keyboards.count_keyboard import get_count
from utilities.find_location.find_city import user_location
from utilities.hotel.find_destination import get_dic_with_cities
from utilities.hotel.check_date import check_user_date
from utilities.hotel.finde_hotels import create_hotels_dict
from utilities.hotel.hotel_photo import get_hotel_photo


class FSMHotels(StatesGroup):
    ask_about_city = State()
    get_city = State()
    get_dates = State()
    count_of_hotels = State()
    sort_hotels = State()
    get_dic_with_hotels = State()


async def start_search_hotels(message: types.Message):
    """
    Начинает процесс поиска отелей.
    Отправляет пользователю сообщение с просьбой ввести город или отправить геолокацию.

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.

    Действие:
        Инициирует начало процесса поиска отелей и устанавливает первое состояние FSMHotels.ask_about_city.
    """
    location_keyboard = await location_button() # Создание клавиатуры
    await bot.send_message(message.from_user.id, 'Введите пожалуйста город, или отправьте геолокацию.'
                                                 '\nПока не работает для России и Беларуси.',
                           reply_markup=location_keyboard)
    await FSMHotels.ask_about_city.set()


async def city_to_search(message: types.Message, state: FSMContext):
    """
    Обрабатывает выбранный пользователем город для поиска отелей.
    Извлекает данные о городе и формирует список городов для выбора пользователем.
    Формируется клавиатура для выбора города. (keyboard = await cities_button_generator(ask_about_city))

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.
        state (FSMContext): Контекст состояния конечного автомата для управления диалогом с пользователем.

    Действие:
        Обновляет состояние FSMHotels.ask_about_city и предоставляет пользователю список городов для выбора.
    """
    city_name = await user_location(message) # Получаем название города по локации или текстовому вводу
    search_result = await get_dic_with_cities(city_name) # Получает информацию о городе из API Booking.com.
    async with state.proxy() as ask_about_city:
        for result in search_result:
            if 'dest_type' in result and result['dest_type'] == 'city':
                ask_about_city[result["label"][:33]] = result
    await state.update_data(city_info=ask_about_city)
    keyboard = await cities_button_generator(ask_about_city) # Генерация инлайн-кнопок с городами
    await FSMHotels.next()
    await bot.send_message(message.from_user.id, f'Ищу ваш город: {city_name.capitalize()}',
                           reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, f'Пожалуйста выберите один из вариантов: ',
                           reply_markup=keyboard)


async def get_city_id(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор города из списка после нажатия на кнопку в инлайн-клавиатуре.
    Получает ID выбранного города и переходит к следующему шагу для запроса дат заезда и выезда.

    Параметры:
        callback (types.CallbackQuery): Объект события от Telegram с информацией о нажатии на кнопку.
        state (FSMContext): Контекст состояния конечного автомата для управления диалогом с пользователем.

    Действие:
        Извлекает информацию о городе из состояния, обновляет данные о выбранном городе в контексте.
        Отправляет пользователю сообщение с информацией о выбранном городе и запрашивает даты заезда и выезда.
        Переходит к следующему шагу FSMHotels.get_dates.
    """
    await callback.answer()
    data = await state.get_data()
    ask_about_city = data.get('city_info', {})
    callback_user_data = callback.data[2:]
    current_city = ask_about_city[callback_user_data]
    async with state.proxy() as data:
        data['city'] = current_city['dest_id']
    await callback.message.answer(f'Ищем отели в: {current_city["label"]}')
    await callback.message.answer('Введите даты заезда и выезда,'
                                  '\nв формате: 00/00/0000-00/00/0000')
    await FSMHotels.next()


async def arrival_dates(message: types.Message, state: FSMContext):
    """
    Обрабатывает введенные пользователем даты заезда и выезда.
    Проверяет корректность введенного формата даты и предоставляет пользователю возможность редактировать даты.

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.
        state (FSMContext): Контекст состояния конечного автомата для управления диалогом с пользователем.

    Действие:
        Проверяет введенные даты на корректность. Если даты некорректные, отправляет пользователю сообщение об ошибке.
        Если даты корректные, сохраняет их в контексте и предоставляет пользователю возможность редактировать даты.
        Переходит к следующему шагу FSMHotels.get_count.
    """
    yes_no_keyboard = await yes_no_checker() # Создание клавиатуры
    user_date = await check_user_date(message.text) #Проверка даты на корректный ввод
    if user_date is False:
        await bot.send_message(message.from_user.id, 'Ошибка ввода даты. Повторите пожалуйста.')
    else:
        await bot.send_message(message.from_user.id, f'Ваши даты бронирования:'
                                                     f'\nДата заезда: {user_date[0]}'
                                                     f'\nДата выезда: {user_date[1]}')
        async with state.proxy() as data:
            data['dates'] = user_date
        await bot.send_message(message.from_user.id, 'Редактировать даты ?', reply_markup=yes_no_keyboard)
        await FSMHotels.next()


async def get_hotels_count(callback: types.CallbackQuery):
    """
    Обрабатывает выбор количества отелей для вывода после нажатия на кнопку в инлайн-клавиатуре.
    Переходит к следующему шагу для запроса дополнительной информации о выборе отелей.

    Параметры:
        callback (types.CallbackQuery): Объект события от Telegram с информацией о нажатии на кнопку.

    Действие:
        Если пользователь выбирает редактировать даты, отправляет запрос на ввод новых дат.
        Иначе предоставляет пользователю выбор количества отелей для вывода.
        Переходит к следующему шагу FSMHotels.count_of_hotels.
    """
    await callback.answer()
    if callback.data == '//да':
        await callback.message.answer('Введите пожалуйста новые даты.')
        await FSMHotels.get_dates.set()
    else:
        keyboard_count = await get_count()
        await callback.message.answer('Пожалуйста выберите сколько вывести отелей:', reply_markup=keyboard_count)
        await FSMHotels.next()


async def sort_hotels(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает выбор сортировки отелей по рейтингу после нажатия на кнопку в инлайн-клавиатуре.
    Получает выбранный пользователем параметр сортировки и переходит к следующему шагу для поиска отелей.

    Параметры:
        callback (types.CallbackQuery): Объект события от Telegram с информацией о нажатии на кнопку.
        state (FSMContext): Контекст состояния конечного автомата для управления диалогом с пользователем.

    Действие:
        Извлекает информацию о количестве отелей из состояния, сохраняет выбранный пользователем параметр сортировки.
        Отправляет пользователю сообщение с вопросом о выборе способа сортировки отелей и переходит к следующему шагу FSMHotels.get_dic_with_hotels.
    """
    await callback.answer()
    rating_keyboard = await rating_button()
    async with state.proxy() as data:
        data['count'] = int(callback.data[2:])
    await callback.message.answer('Как вывести отели ?:'
                                  '\nНачать с высокого рейтинга'
                                  '\nНачать с низкого рейтинга', reply_markup=rating_keyboard)
    await FSMHotels.next()


async def find_hotels(callback: types.CallbackQuery, state: FSMContext):
    """
    Обрабатывает результаты поиска и вывода отелей после нажатия на кнопку в инлайн-клавиатуре.
    Выводит результаты поиска отелей и завершает диалог с пользователем.

    Параметры:
        callback (types.CallbackQuery): Объект события от Telegram с информацией о нажатии на кнопку.
        state (FSMContext): Контекст состояния конечного автомата для управления диалогом с пользователем.

    Действие:
        Извлекает информацию о параметрах поиска отелей и получает список отелей с заданными параметрами.
        Если найдены отели, выводит информацию о каждом отеле, включая фотографии, оценку, класс и даты.
        Если не найдено отелей, отправляет сообщение с соответствующим уведомлением.
        Завершает диалог с пользователем и предоставляет возможность выбрать другой пункт меню.
    """
    await callback.answer()
    if callback.data in ['//больше', '//меньше']:
        start_keyboard = await start_button()
        async with state.proxy() as data:
            data['rating'] = True if callback.data == '//больше' else False

            hotels_list = await create_hotels_dict(data['city'],
                                                   data['dates'][0],
                                                   data['dates'][1],
                                                   data['rating'],
                                                   data['count'],
                                                   'class_descending' if data['rating'] is True
                                                   else 'class_ascending')

            if len(hotels_list) == 0:
                await callback.message.answer(f'Извините, для вашего города не поддерживается поиск отелей')
            else:
                if len(hotels_list) < data['count']:
                    await callback.message.answer(f'Извините я не смог найти {data["count"]} отелей.')
                await callback.message.answer('Отели которые я нашёл: ')

                for hotel in hotels_list:
                    photo = await get_hotel_photo(hotel['hotel_id'])
                    media_group = [types.InputMediaPhoto(url) for url in photo]
                    await callback.message.answer_media_group(media_group)
                    await callback.message.answer(f'{hotel["hotel_name"]}'
                                                  f'\nОценка: {hotel["review_score"]} - {hotel["review_score_word"]}'
                                                  f'\nКоличество звёзд: {round(hotel["class"], 0)}'
                                                  f'\nЗаезд: c {hotel["checkin"]["until"]} '
                                                  f'по {hotel["checkin"]["from"]}'
                                                  f'\nВыезд: с {hotel["checkout"]["from"]} '
                                                  f'по {hotel["checkout"]["until"]}'
                                                  f'\nСсылка: {hotel["url"]}', disable_web_page_preview=True)
                    await asyncio.sleep(1.0)

        await state.finish()
        await callback.message.answer('Выберите пожалуйста один из пунктов меню, для продолжения',
                                      reply_markup=start_keyboard)
    else:
        await callback.message.answer('Для продолжения нужно выбрать один из вариантов')
        await FSMHotels.sort_hotels.set()


async def cancel(message: types.Message, state: FSMContext):
    """
    Обрабатывает команду отмены действия и возвращает пользователя в главное меню.

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.
        state (FSMContext): Контекст состояния конечного автомата для управления диалогом с пользователем.

    Действие:
        Отправляет сообщение о возврате в главное меню и завершает текущее состояние конечного автомата.
    """
    back_button = await start_button()
    await bot.send_message(message.from_user.id, 'Возврат в главное меню', reply_markup=back_button)
    await state.finish()


def register_handler_hotels(dp: Dispatcher):
    """
    Регистрирует обработчики команд и сообщений для функций, связанных с поиском отелей.

    Параметры:
        dp (Dispatcher): Объект диспетчера от Aiogram для регистрации обработчиков.

    Действие:
        Регистрирует обработчик команды "/Отель" для запуска функции start_search_hotels.
        Регистрирует обработчик выбора города для функции city_to_search
            в состоянии FSMHotels.ask_about_city.
        Регистрирует обработчик колбэк-запроса для получения идентификатора города для функции get_city_id
            с префиксом "//" и в состоянии FSMHotels.get_city.
        Регистрирует обработчик сообщений для запроса даты заезда для функции arrival_dates
            в состоянии FSMHotels.get_dates.
        Регистрирует обработчик колбэк-запроса для выбора количества отелей для функции get_hotels_count
            в состоянии FSMHotels.count_of_hotels.
        Регистрирует обработчик колбэк-запроса для сортировки отелей для функции sort_hotels
            в состоянии FSMHotels.sort_hotels.
        Регистрирует обработчик колбэк-запроса для начала поиска отелей для функции find_hotels
            с префиксом "//" и в состоянии FSMHotels.get_dic_with_hotels.
        Регистрирует обработчик текстового сообщения "отмена" для функции cancel в любом состоянии.
    """
    dp.register_message_handler(start_search_hotels, commands=['Отель'])
    dp.register_message_handler(city_to_search, content_types=['text', 'location'], state=FSMHotels.ask_about_city)
    dp.register_callback_query_handler(get_city_id, Text(startswith='//'), state=FSMHotels.get_city)
    dp.register_message_handler(arrival_dates, state=FSMHotels.get_dates)
    dp.register_callback_query_handler(get_hotels_count, state=FSMHotels.count_of_hotels)
    dp.register_callback_query_handler(sort_hotels, state=FSMHotels.sort_hotels)
    dp.register_callback_query_handler(find_hotels, Text(startswith='//'),
                                       state=FSMHotels.get_dic_with_hotels)
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
