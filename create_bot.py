from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage_for_answer = MemoryStorage()

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
weather_key = os.getenv('WEATHER_TOKEN')
hotel_key = os.getenv('HOTEL_KEY')
rest_key = os.getenv('REST_KET')
dp = Dispatcher(bot, storage=storage_for_answer)
