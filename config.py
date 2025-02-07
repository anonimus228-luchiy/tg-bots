from decouple import config
from aiogram import Bot, Dispatcher
from decouple import config

token = config("BOT_TOKEN")
bot = Bot(token=token)
dp = Dispatcher(bot)



Admins = [995712956, ]
