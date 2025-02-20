<<<<<<< HEAD
# config.py
=======
import logging
>>>>>>> b638d0a829cd41a6d12c7914c738a72fc75d1952
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config
from aiogram.contrib.fsm_storage.memory import MemoryStorage

token = config("TOKEN")

<<<<<<< HEAD
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

Admins = [7041912200, ]
=======
TOKEN = config("BOT_TOKEN")
storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(level=logging.INFO)
>>>>>>> b638d0a829cd41a6d12c7914c738a72fc75d1952
