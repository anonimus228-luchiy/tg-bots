from aiogram import types, Dispatcher
from config import bot
<<<<<<< HEAD:handlers/commands.py
import buttons

=======
import handlers.shop
from aiogram.utils import executor
from config import dp
>>>>>>> b638d0a829cd41a6d12c7914c738a72fc75d1952:commands.py

async def start_hanler(message: types.Message):
    print('Обработчик старта')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Hello {message.from_user.first_name}\n'
                                f'Твой Telegram ID - {message.from_user.id}\n', reply_markup=buttons.start)

    await message.answer('Привет мир')


async def mem_handler(message: types.Message):
    # photo = open('media/images.jpeg', 'rb')

    with open('media/images.jpeg', 'rb') as photo:
        await bot.send_photo(chat_id=message.from_user.id,
                             photo=photo)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_hanler, commands=['start'])
    dp.register_message_handler(mem_handler, commands=['mem'])



if __name__ == '__main__':
    register_handlers(dp)
    executor.start_polling(dp, skip_updates=True)