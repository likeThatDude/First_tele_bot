from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.location_button import location_button
from utilities.find_city import user_location
from utilities.find_destination import get_dic_with_cities
from keyboards.cities_button import cities_button_generator
from aiogram.dispatcher.filters import Text


dic_with_cities = {}


class FSMHotels(StatesGroup):
    ask_about_city = State()
    get_city = State()
    get_dates = State()
    pass


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
            dic_with_cities[result["label"]] = result
    keyboard = await cities_button_generator(dic_with_cities)
    await FSMHotels.next()
    await bot.send_message(message.from_user.id, f'Вот что я нашёл по вашему запросу: ',
                           reply_markup=keyboard)


async def get_city_id(callback: types.CallbackQuery):
    callback_user_data = callback.data[6:]
    current_city = dic_with_cities[callback_user_data]
    print(current_city)
    await callback.message.answer(f'Я вас понял, ищу отели в: {callback_user_data}')
    await callback.message.answer('Введите даты заезда и выезда,'
                                  '\nв формате: 00/00/0000-00/00/0000')
    await FSMHotels.next()


async def arrival_dates(message: types.Message):
    await bot.send_message(message.from_user.id, f'Ваш текст: {message.text}')
    pass


def register_handler_hotels(dp: Dispatcher):
    dp.register_message_handler(start_search_hotels, commands=['Отель'])
    dp.register_message_handler(city_to_search, content_types=['text', 'location'], state=FSMHotels.ask_about_city)
    dp.register_callback_query_handler(get_city_id, Text(startswith='city: '), state=FSMHotels.get_city)
    dp.register_message_handler(arrival_dates, state=FSMHotels.get_dates)
