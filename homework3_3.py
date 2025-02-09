import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from decouple import config

TOKEN = config("TOKEN")
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

logging.basicConfig(level=logging.INFO)


class ProductState(StatesGroup):
    name = State()
    category = State()
    photo = State()
    size = State()
    price = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! Введите название товара:")
    await ProductState.name.set()


@dp.message_handler(state=ProductState.name)
async def get_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Введите категорию товара:")
    await ProductState.next()


@dp.message_handler(state=ProductState.category)
async def get_category(message: types.Message, state: FSMContext):
    await state.update_data(category=message.text)
    await message.answer("Отправьте фото товара:")
    await ProductState.next()


@dp.message_handler(content_types=['photo'], state=ProductState.photo)
async def get_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await message.answer("Введите размер товара:")
    await ProductState.next()


@dp.message_handler(state=ProductState.size)
async def get_size(message: types.Message, state: FSMContext):
    await state.update_data(size=message.text)
    await message.answer("Введите стоимость товара:")
    await ProductState.next()


@dp.message_handler(state=ProductState.price)
async def get_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    data = await state.get_data()

    response = (f"🛒 Товар добавлен в магазин!\n"
                f"Название: {data['name']}\n"
                f"Категория: {data['category']}\n"
                f"Размер: {data['size']}\n"
                f"Цена: {data['price']} руб.")

    await bot.send_photo(chat_id=message.chat.id, photo=data['photo'], caption=response)
    await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
