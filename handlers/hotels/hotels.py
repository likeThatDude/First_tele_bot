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
from keyboards.hotels_count_keyboard import get_count
from utilities.find_location.find_city import user_location
from utilities.hotel.find_destination import get_dic_with_cities
from utilities.hotel.check_date import check_user_date
from utilities.hotel.finde_hotels import create_hotels_dict
from utilities.hotel.hotel_photo import get_hotel_photo

dic_with_cities = {}
dic_with_user_answers = {}


class FSMHotels(StatesGroup):
    ask_about_city = State()
    get_city = State()
    get_dates = State()
    count_of_hotels = State()
    sort_hotels = State()
    get_dic_with_hotels = State()


async def start_search_hotels(message: types.Message):
    location_keyboard = await location_button()
    await bot.send_message(message.from_user.id, 'Введите пожалуйста город, или отправьте геолокацию.'
                                                 '\nПока не работает для России и Беларуси.',
                           reply_markup=location_keyboard)
    await FSMHotels.ask_about_city.set()


async def city_to_search(message: types.Message):
    global dic_with_cities
    city_name = await user_location(message)
    search_result = await get_dic_with_cities(city_name)
    for result in search_result:
        if 'dest_type' in result and result['dest_type'] == 'city':
            dic_with_cities[result["label"][:33]] = result
    keyboard = await cities_button_generator(dic_with_cities)
    await FSMHotels.next()
    await bot.send_message(message.from_user.id, f'Ищу ваш город: {city_name.capitalize()}',
                           reply_markup=types.ReplyKeyboardRemove())
    await bot.send_message(message.from_user.id, f'Пожалуйста выберите один из вариантов: ',
                           reply_markup=keyboard)


async def get_city_id(callback: types.CallbackQuery):
    await callback.answer()
    callback_user_data = callback.data[2:]
    current_city = dic_with_cities[callback_user_data]
    dic_with_user_answers['city'] = current_city['dest_id']
    await callback.message.answer(f'Ищем отели в: {current_city["label"]}')
    await callback.message.answer('Введите даты заезда и выезда,'
                                  '\nв формате: 00/00/0000-00/00/0000')
    await FSMHotels.next()


async def arrival_dates(message: types.Message):
    yes_no_keyboard = await yes_no_checker()
    user_date = await check_user_date(message.text)
    if user_date is False:
        await bot.send_message(message.from_user.id, 'Ошибка ввода даты. Повторите пожалуйста.')
    else:
        await bot.send_message(message.from_user.id, f'Ваши даты бронирования:'
                                                     f'\nДата заезда: {user_date[0]}'
                                                     f'\nДата выезда: {user_date[1]}')
        dic_with_user_answers['dates'] = user_date
        await bot.send_message(message.from_user.id, 'Редактировать даты ?', reply_markup=yes_no_keyboard)
        await FSMHotels.next()


async def get_hotels_count(callback: types.CallbackQuery):
    await callback.answer()
    if callback.data == '//да':
        await callback.message.answer('Введите пожалуйста новые даты.')
        await FSMHotels.get_dates.set()
    else:
        keyboard_count = await get_count()
        await callback.message.answer('Пожалуйста выберите сколько вывести отелей:', reply_markup=keyboard_count)
        await FSMHotels.next()


async def sort_hotels(callback: types.CallbackQuery):
    await callback.answer()
    rating_keyboard = await rating_button()
    dic_with_user_answers['count'] = int(callback.data[2:])
    await callback.message.answer('Как вывести отели ?:'
                                  '\nНачать с высокого рейтинга'
                                  '\nНачать с низкого рейтинга', reply_markup=rating_keyboard)
    await FSMHotels.next()


async def find_hotels(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    if callback.data in ['//больше', '//меньше']:
        start_keyboard = await start_button()
        dic_with_user_answers['rating'] = True if callback.data == '//больше' else False

        hotels_list = await create_hotels_dict(dic_with_user_answers['city'],
                                               dic_with_user_answers['dates'][0],
                                               dic_with_user_answers['dates'][1],
                                               dic_with_user_answers['rating'],
                                               dic_with_user_answers['count'],
                                               'class_descending' if dic_with_user_answers['rating'] is True
                                               else 'class_ascending')

        if len(hotels_list) == 0:
            await callback.message.answer(f'Извините, для вашего города: {dic_with_user_answers["city"]}, '
                                          f'не поддерживается поиск отелей')
        else:
            if len(hotels_list) < dic_with_user_answers['count']:
                await callback.message.answer(f'Извините я не смог найти {dic_with_user_answers["count"]} отелей.')
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


def register_handler_hotels(dp: Dispatcher):
    dp.register_message_handler(start_search_hotels, commands=['Отель'])
    dp.register_message_handler(city_to_search, content_types=['text', 'location'], state=FSMHotels.ask_about_city)
    dp.register_callback_query_handler(get_city_id, Text(startswith='//'), state=FSMHotels.get_city)
    dp.register_message_handler(arrival_dates, state=FSMHotels.get_dates)
    dp.register_callback_query_handler(get_hotels_count, state=FSMHotels.count_of_hotels)
    dp.register_callback_query_handler(sort_hotels, state=FSMHotels.sort_hotels)
    dp.register_callback_query_handler(find_hotels, Text(startswith='//'),
                                       state=FSMHotels.get_dic_with_hotels)
