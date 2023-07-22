from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
import os

load_dotenv()
bot = Bot(token=os.getenv('BOT_TOKEN'))
weather_key = os.getenv('WEATHER_TOKEN')
dp = Dispatcher(bot)
