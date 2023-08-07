from create_bot import bot
from datetime import datetime
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.start_keyboard import start_button


async def start_command(message: types.Message):
    """
    Обработчик команды "/start".

    Эта функция вызывается, когда пользователь отправляет боту команду "/start".
    Она приветствует пользователя в зависимости от текущего времени и предоставляет список функций, которые бот может выполнить.

    Параметры:
        message (types.Message): Объект сообщения от пользователя.

    Примечание:
        Для корректной работы этой функции необходимо импортировать модуль "types" из библиотеки "aiogram",
        а также создать экземпляр бота "bot" из модуля "create_bot" и импортировать функцию "start_button" из модуля "keyboards.start_keyboard".

    Пример использования:
        Пользователь отправляет команду "/start", и бот приветствует его и предоставляет список доступных функций.

    """

    current_time = datetime.now().time()
    hour = current_time.hour

    if 4 <= hour < 10:
        time_period = "Доброе утро"
    elif 10 <= hour < 17:
        time_period = "Добрый день"
    elif 17 <= hour < 23:
        time_period = "Добрый вечер"
    else:
        time_period = "Доброй ночь"

    start_keyboard = await start_button()
    await bot.send_message(message.from_user.id, f'{time_period}, {message.from_user.first_name} !\n'
                                                 f'\nЯ бот помощник, у меня есть следующие функции: '
                                                 f'\n1) Поиск отелей. 🏨'
                                                 f'\n2) Поиск ресторанов, кафе.🍜'
                                                 f'\n3) Могу узнать погоду в интересующем вас городе.🌦',
                           reply_markup=start_keyboard)


async def cancel(message: types.Message, state: FSMContext):
    back_button = await start_button()
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(message.from_user.id, 'Вы уже в главном меню.'
                                                     '\nПросто вызовите клавиатуру около поля ввода текста')
    else:
        await bot.send_message(message.from_user.id, 'Возврат в главное меню', reply_markup=back_button)
        await state.finish()


def register_handler_start(dp: Dispatcher):
    """
    Регистрация обработчика команды "/start" в диспетчере.

    Эта функция регистрирует обработчик "start_command" для команды "/start" в диспетчере бота.

    Параметры:
        dp (Dispatcher): Объект диспетчера из библиотеки "aiogram".

    Примечание:
        Функция "start_command" должна быть определена и иметь аргумент "message" типа "types.Message".
        Для корректной работы этой функции необходимо импортировать модуль "Dispatcher" из библиотеки "aiogram".

    Пример использования:
        Регистрация обработчика команды "/start" в диспетчере для дальнейшей обработки данной команды от пользователя.

    """
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
