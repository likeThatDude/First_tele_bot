from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from keyboards.location_button import location_button
from utilities.find_city import user_location
from utilities.find_destination import get_dic_with_cities
from keyboards.cities_button import cities_button_generator
from aiogram.dispatcher.filters import Text
from utilities.check_date import check_user_date
from utilities.finde_hotels import create_hotels_dict

dic_with_cities = {}
dic_with_user_answers = {}


class FSMHotels(StatesGroup):
    ask_about_city = State()
    get_city = State()
    get_dates = State()
    get_dic_with_hotels = State()


async def start_search_hotels(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите пожалуйста город, в котором будем искать отель.'
                                                 '\nИли можете отправить свою геолокацию,'
                                                 '\nя найду отели в городе вашего нахождения.',
                           reply_markup=location_button)
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
    await bot.send_message(message.from_user.id, f'Вот что я нашёл по вашему запросу: ',
                           reply_markup=keyboard)


async def get_city_id(callback: types.CallbackQuery):
    callback_user_data = callback.data[2:]
    current_city = dic_with_cities[callback_user_data]
    dic_with_user_answers['city'] = current_city['dest_id']
    await callback.message.answer(f'Ищем отели в: {current_city["label"]}')
    await callback.message.answer('Введите даты заезда и выезда,'
                                  '\nв формате: 00/00/0000-00/00/0000')
    await FSMHotels.next()


async def arrival_dates(message: types.Message):
    user_date = await check_user_date(message.text)
    if user_date is False:
        bot.send_message(message.from_user.id, 'Ошибка ввода даты. Повторите пожалуйста.')
    else:
        await bot.send_message(message.from_user.id, f'Ваши даты бронирования:'
                                                     f'\nДата заезда: {user_date[0]}'
                                                     f'\nДата выезда: {user_date[1]}')
        dic_with_user_answers['dates'] = user_date
        await FSMHotels.next()


async def find_hotels(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вот ваши отели')
    hotels_list = await create_hotels_dict(dic_with_user_answers['city'],
                                           dic_with_user_answers['dates'][0],
                                           dic_with_user_answers['dates'][1])
    for hotel_name in hotels_list:
        await bot.send_message(message.from_user.id, hotel_name['name'])


def register_handler_hotels(dp: Dispatcher):
    dp.register_message_handler(start_search_hotels, commands=['Отель'])
    dp.register_message_handler(city_to_search, content_types=['text', 'location'], state=FSMHotels.ask_about_city)
    dp.register_callback_query_handler(get_city_id, Text(startswith='//'), state=FSMHotels.get_city)
    dp.register_message_handler(arrival_dates, state=FSMHotels.get_dates)
    dp.register_message_handler(find_hotels, state=FSMHotels.get_dic_with_hotels)
