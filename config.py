import os
from aiogram import Bot, Dispatcher
from decouple import config

env_path = os.path.join(os.path.dirname(__file__), '.env')
if not os.path.exists(env_path):
    raise FileNotFoundError(
        f'.env файл не найден по пути {env_path}. '
        f'Пожалуйста, создайте файл .env и добавьте в него BOT_TOKEN=ваш_токен'
    )

token = config("BOT_TOKEN")
if not token:
    raise ValueError(
        'BOT_TOKEN не найден в .env файле. '
        'Пожалуйста, добавьте BOT_TOKEN=ваш_токен в файл .env'
    )

bot = Bot(token=token)
dp = Dispatcher(bot)

Admins = [7041912200,]