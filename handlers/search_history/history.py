from create_bot import bot
from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.start_keyboard import start_button
from data_base.sqlite_db import get_history


async def history_start(message: types.Message):
    start_keyboard = await start_button()
    await bot.send_message(message.from_user.id, 'Добро пожаловать в меню истории запросов. '
                                                 '\nВот ваши последние запросы:')

    user_data = await get_history(message.from_user.id)
    if len(user_data) > 0:
        for i in user_data:
            await bot.send_message(message.from_user.id, f'\n_________________'
                                                         f'\nКАТЕГОРИЯ ПОИСКА: '
                                                         f'\n{i[0]}'
                                                         f'\n-----------------'
                                                         f'\nЗАПРОС: '
                                                         f'\n{i[1]}'
                                                         f'\n-----------------'
                                                         f'\nДАТА ЗАПРОСА: '
                                                         f'\n{i[2]}'
                                                         f'\n_________________')
    else:
        await bot.send_message(message.from_user.id, f'{message.from_user.first_name}, у вас пока нету запросов.')
    await bot.send_message(message.from_user.id, 'Для продолжения выберите один из пунктов меню: ',
                           reply_markup=start_keyboard)


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
    dp.register_message_handler(history_start, commands=['История_запросов'])
    dp.register_message_handler(cancel, Text(equals='отмена', ignore_case=True), state='*')
