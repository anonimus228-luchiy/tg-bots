from aiogram import types, Dispatcher
from config import bot
from db import main_db
from fsm_store.fsm_store import StoreStates
from aiogram.dispatcher import FSMContext

async def fsm_start(message: types.Message):
    await StoreStates.name_product.set()
    await message.answer("Введите название продукта")

async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text
    await StoreStates.size.set()
    await message.answer("Введите размер")

async def load_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size'] = message.text
    await StoreStates.price.set()
    await message.answer("Введите цену")

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = float(message.text)
    await StoreStates.photo.set()
    await message.answer("Отправьте фото")

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await StoreStates.productid.set()
    await message.answer("Введите ID продукта")

async def load_productid(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['productid'] = int(message.text)
    await StoreStates.category.set()
    await message.answer("Введите категорию")

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text
    await StoreStates.infoproduct.set()
    await message.answer("Введите информацию о продукте")

async def load_infoproduct(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['infoproduct'] = message.text
        
    # Сохраняем в старые таблицы
    await main_db.sql_insert_store(
        data['name_product'],
        data['size'],
        data['price'],
        data['photo'],
        data['productid']
    )
    
    await main_db.sql_insert_store_detail(
        data['productid'],
        data['infoproduct'],
        data['category']
    )
    
    # Сохраняем в новые таблицы
    await main_db.sql_insert_products(
        data['name_product'],
        data['size'],
        data['price'],
        data['photo'],
        data['productid']
    )
    
    await main_db.sql_insert_products_details(
        data['productid'],
        data['category'],
        data['infoproduct']
    )
    if fsm_start:
        await bot.delete_message(message.chat.id, message.message_id)
    await message.answer("Данные сохранены!")
    await state.finish()

def register_handlers_fsm_store(dp: Dispatcher):
    dp.register_message_handler(fsm_start, commands=['store'])
    dp.register_message_handler(load_name_product, state=StoreStates.name_product)
    dp.register_message_handler(load_size, state=StoreStates.size)
    dp.register_message_handler(load_price, state=StoreStates.price)
    dp.register_message_handler(load_photo, content_types=['photo'], state=StoreStates.photo)
    dp.register_message_handler(load_productid, state=StoreStates.productid)
    dp.register_message_handler(load_category, state=StoreStates.category)
    dp.register_message_handler(load_infoproduct, state=StoreStates.infoproduct)