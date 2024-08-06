from datetime import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from create_bot import bot
from data_base.sqlite_db import add_user
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
    await add_user(message.from_user.id, message.from_user.first_name)

    if 4 <= hour < 10:
        time_period = "Доброе утро"
    elif 10 <= hour < 17:
        time_period = "Добрый день"
    elif 17 <= hour < 23:
        time_period = "Добрый вечер"
    else:
        time_period = "Доброй ночь"

    start_keyboard = await start_button()
    await bot.send_message(
        message.from_user.id,
        f"{time_period}, {message.from_user.first_name} !\n"
        f"\nЯ бот помощник, у меня есть следующие функции: "
        f"\n1) Поиск отелей. 🏨"
        f"\n2) Поиск ресторанов, кафе.🍜"
        f"\n3) Могу узнать погоду в интересующем вас городе.🌦",
        reply_markup=start_keyboard,
    )


async def cancel(message: types.Message, state: FSMContext):
    """
    Функция для отмены текущего состояния и возврата в главное меню.

    Параметры:
        message (types.Message): Объект события от Telegram с информацией о сообщении пользователя.
        state (FSMContext): Объект состояния конечного автомата для завершения текущего состояния.

    Действие:
        Если пользователь находится в активном состоянии (не в главном меню), отправляет ему уведомление
        о возврате в главное меню и предоставляет кнопку для этого.
        Завершает текущее состояние конечного автомата, чтобы вернуться в исходное состояние (главное меню).
        Если пользователь уже находится в главном меню, уведомляет его об этом.
    """
    back_button = await start_button()
    current_state = await state.get_state()
    if current_state is None:
        await bot.send_message(
            message.from_user.id,
            "Вы уже в главном меню."
            "\nПросто вызовите клавиатуру около поля ввода текста",
        )
    else:
        await bot.send_message(
            message.from_user.id,
            "Возврат в главное меню",
            reply_markup=back_button,
        )
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
    dp.register_message_handler(start_command, commands=["start"])
    dp.register_message_handler(
        cancel, Text(equals="отмена", ignore_case=True), state="*"
    )
