import asyncio
from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from keyboards.location_button import location_button
from keyboards.count_keyboard import get_count
from keyboards.start_keyboard import start_button
from utilities.find_location.find_city import user_location
from utilities.restaurants.get_city_id import get_city_id
from utilities.restaurants.get_rest_list import get_rest_list


class FSMRest(StatesGroup):
    city = State()
    rest_count = State()
    show_result = State()


async def rest_start(message: types.Message):
    keyboard = await location_button()
    await bot.send_message(message.from_user.id,
                           'Введите город, или отправьте свою геолокацию, для поиска лучших ресторанов в городе.',
                           reply_markup=keyboard)
    await FSMRest.city.set()


async def user_choice(message: types.Message, state: FSMContext):
    city_name = await user_location(message)
    async with state.proxy() as data:
        city_id = await get_city_id(city_name)
        data['city_name'] = city_name
        data['city_id'] = city_id
    keyboard = await get_count()
    await bot.send_message(message.from_user.id, f'Какое количество ресторанов найти ?', reply_markup=keyboard)
    await FSMRest.next()


async def get_rest_count(callback: types.CallbackQuery, state: FSMContext):
    await callback.answer()
    rest_count = int(callback.data[2:])
    async with state.proxy() as data:
        list_with_restaurants = await get_rest_list(data['city_id'], rest_count)
        data['restaurants'] = list_with_restaurants
        await callback.message.answer(f'Вот лучшие рестораны в городе: {data["city_name"]}')
        for restaurant in data['restaurants']:
            await bot.send_photo(restaurant['photo']['images']['original']['url'])
            await callback.message.answer(f'Название: {restaurant["name"]}'
                                          f'\nПозиция в рейтинге: {restaurant["ranking_position"]}'
                                          f'\nРейтинг: {restaurant["rating"]}'
                                          f'\nСейчас: {restaurant["open_now_text"]}\n'
                                          f'\nКонтакты:'
                                          f'\nТелефон: {restaurant["phone"]}'
                                          f'\nemail: {restaurant["email"]}'
                                          f'\nадрес: {restaurant["address"]}'
                                          f'\nДля более подробной информации'
                                          f'\nпройдите по ссылке:'
                                          f'\n{restaurant["web_url"]}', disable_web_page_preview=True)
            await asyncio.sleep(1.0)
    await state.finish()


async def cancel(message: types.Message, state: FSMContext):
    back_button = await start_button()
    await bot.send_message(message.from_user.id, 'Возврат в главное меню', reply_markup=back_button)
    await state.finish()


def register_handler_hotels(dp: Dispatcher):
    dp.register_message_handler(rest_start, commands=['Рестораны'])
    dp.register_message_handler(user_choice, content_types=['text', 'location'], state=FSMRest.city)
    dp.register_callback_query_handler(get_rest_count, Text(startswith='//'), state=FSMRest.rest_count)
    dp.register_message_handler(cancel,Text(equals='отмена', ignore_case=True), state='*')
