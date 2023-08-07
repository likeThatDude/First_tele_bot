import asyncio
from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.count_keyboard import get_count
from keyboards.start_keyboard import start_button
from keyboards.location_button import location_button
from utilities.restaurants.get_city_id import get_city_id
from utilities.restaurants.get_rest_list import get_rest_list
from utilities.find_location.find_city import user_location


class FSMRest(StatesGroup):
    city = State()
    rest_count = State()
    show_result = State()


async def rest_start(message: types.Message):
    """
    Функция, которая запускается при команде "/Рестораны".
    Она запрашивает у пользователя название города или просит поделиться геолокацией.

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.

    Действие:
        Отправляет сообщение пользователю с текстом о запросе названия города или поделиться местоположением.
        В сообщении будет также прикреплена пользовательская клавиатура с кнопкой "Отправить местоположение".
        Задает состояние FSMRest.city для следующего шага конечного автомата.
    """
    keyboard = await location_button()
    await bot.send_message(message.from_user.id,
                           'Введите город, или отправьте свою геолокацию, для поиска лучших ресторанов в городе.',
                           reply_markup=keyboard)
    await FSMRest.city.set()


async def user_choice(message: types.Message, state: FSMContext):
    """
    Функция, которая обрабатывает выбор пользователя по городу и количеству ресторанов.
    Она получает название города от пользователя, проверяет его наличие, затем запрашивает количество ресторанов.

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.
        state (FSMContext): Объект состояния конечного автомата для сохранения промежуточных данных.

    Действие:
        Если указанный город существует, сохраняет данные о городе и его идентификаторе в состоянии конечного автомата.
        Отправляет пользователю запрос о количестве ресторанов с клавиатурой для выбора количества.
        Переводит конечный автомат в следующее состояние для ожидания ответа по количеству ресторанов.
        Если город не найден, уведомляет пользователя об ошибке поиска и предлагает попробовать снова или вернуться в главное меню.
    """
    city_name = await user_location(message) # Получение название города
    city_id = await get_city_id(city_name) # Получение id города в сервисе Worldwide Restaurants
    if city_id is not False:
        async with state.proxy() as data:
            data['city_name'] = city_name
            data['city_id'] = city_id
        keyboard = await get_count()
        await bot.send_message(message.from_user.id, f'Какое количество ресторанов найти ?', reply_markup=keyboard)
        await FSMRest.next()
    else:
        await bot.send_message(message.from_user.id, f'Ошибка поиска города.'
                                                     f'\nПопробуйте ввести заново или'
                                                     f'\nвведите << отмена >> для возврата в главное меню.')



async def get_rest_count(callback: types.CallbackQuery, state: FSMContext):
    """
    Функция, которая обрабатывает выбор количества ресторанов и выводит информацию о них.
    Она получает колбэк-запрос от пользователя, а также состояние конечного автомата.

    Параметры:
        callback (types.CallbackQuery): Объект события от Telegram с информацией о колбэк-запросе пользователя.
        state (FSMContext): Объект состояния конечного автомата для доступа к промежуточным данным.

    Действие:
        Отвечает на колбэк-запрос, сохраняет выбранное количество ресторанов и запрашивает список ресторанов.
        Если успешно получен список ресторанов, выводит информацию о каждом из них пользователю.
        После завершения вывода ресторанов предлагает пользователю выбрать один из вариантов в главном меню.
        Если произошла ошибка поиска ресторанов, уведомляет пользователя и предлагает вернуться в главное меню.
        Завершает состояние конечного автомата.
    """
    await callback.answer()
    rest_count = int(callback.data[2:])
    start_keyboard = await start_button()
    async with state.proxy() as data:
        list_with_restaurants = await get_rest_list(data['city_id'], rest_count)
        if list_with_restaurants is not False:
            data['restaurants'] = list_with_restaurants
            await callback.message.answer(f'Вот лучшие рестораны в городе: {data["city_name"]}')
            for restaurant in data['restaurants']:
                await bot.send_photo(callback.message.chat.id, restaurant['photo']['images']['original']['url'])
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
            await callback.message.answer(f'Для продолжения выберете один из вариантов:', reply_markup=start_keyboard)
        else:
            await callback.message.answer(f'Извините, произошла ошибка поиска ресторанов,'
                                          f'\nвозврат в главное меню.', reply_markup=start_keyboard)
    await state.finish()


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
    Регистрирует обработчики команд и сообщений для функций, связанных с ресторанами.

    Параметры:
        dp (Dispatcher): Объект диспетчера от Aiogram для регистрации обработчиков.

    Действие:
        Регистрирует обработчик команды "/Рестораны" для запуска функции rest_start.
        Регистрирует обработчик выбора города и количества ресторанов для функции user_choice
            в состоянии FSMRest.city.
        Регистрирует обработчик колбэк-запроса для выбора количества ресторанов для функции get_rest_count
            с префиксом "//" и в состоянии FSMRest.rest_count.
        Регистрирует обработчик текстового сообщения "отмена" для функции cancel в любом состоянии.
    """
    dp.register_message_handler(rest_start, commands=['Рестораны'])
    dp.register_message_handler(user_choice, content_types=['text', 'location'], state=FSMRest.city)
    dp.register_callback_query_handler(get_rest_count, Text(startswith='//'), state=FSMRest.rest_count)
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
