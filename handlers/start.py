from aiogram import types, Dispatcher
from create_bot import bot
from keyboards import client_keyboards


async def start_command(message: types.Message):
    await bot.send_message(message.from_user.id, f'Привет, {message.from_user.first_name} !\n'
                                                 f'\nЯ бот помощник, у меня есть следующие функции: '
                                                 f'\n1) Поиск отелей.'
                                                 f'\n2) Поиск ресторанов, кафе.'
                                                 f'\n3) Могу узнать погоду в интересующем вас городе.',
                           reply_markup=client_keyboards)


def register_handler_start(dp: Dispatcher):
    dp.register_message_handler(start_command, commands=['start'])
