from aiogram import types, Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from db import main_db
import buttons
import logging

class StoreFSM(StatesGroup):
    name_product = State()
    size = State()
    price = State()
    category = State()
    info_product = State()
    products_id = State()
    photo = State()
    submit = State()


async def start_fsm_store(message: types.Message):
    if message.chat.type == 'private':
        await StoreFSM.name_product.set()
        await message.answer('Введите название товара:', reply_markup=buttons.cancel_fsm)


async def cancel_fsm_store(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=buttons.start)


async def name_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите размер:')


async def size_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['size_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите цену товара:')


async def price_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите категорию товара:')


async def category_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите информацию о продукте:')


async def info_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['info_product'] = message.text

    await StoreFSM.next()
    await message.answer('Введите артикул для товара: ')


async def product_id_load(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['products_id'] = message.text

    await StoreFSM.next()
    await message.answer("Отправьте фото товара:")


async def photo_load(message: types.Message, state: FSMContext):
    if not message.photo:
        await message.answer("Пожалуйста, отправьте фото!")
        return
    
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id

    await StoreFSM.next()
    await message.answer('Верные ли данные?', reply_markup=buttons.submit)
    await message.answer_photo(
        photo=data['photo'],
        caption=f'Название товара - {data["name_product"]}\n'
                f'Размер товара - {data["size_product"]}\n'
                f'Категория - {data["category_product"]}\n'
                f'Артикул - {data["products_id"]}\n'
                f'Инфо - {data["info_product"]}\n'
                f'Цена - {data["price_product"]}'
    )


async def submit_load(message: types.Message, state: FSMContext):
    try:
        if message.text.lower() not in ['да', 'нет']:
            await message.answer('Пожалуйста, выберите "да" или "нет"')
            return

        if message.text.lower() == 'нет':
            await state.finish()
            await message.answer('Отменено!', reply_markup=buttons.start)
            return

        # Если ответ "да"
        async with state.proxy() as data:
            try:
                # Сначала пробуем вставить в основную таблицу
                await main_db.sql_insert_store(
                    name_product=data['name_product'],
                    size=data['size_product'],
                    price=data['price_product'],
                    product_id=data['products_id'],
                    photo=data['photo']
                )

                # Если успешно, то вставляем в таблицу деталей
                await main_db.sql_insert_store_detail(
                    product_id=data['products_id'],
                    info_product=data['info_product'],
                    category=data['category_product']
                )

                await message.answer('Товар успешно добавлен!', reply_markup=buttons.start)
            except Exception as e:
                logging.error(f"Error in submit_load: {e}")
                await message.answer(
                    'Произошла ошибка при сохранении товара. Возможно, такой артикул уже существует.',
                    reply_markup=buttons.start
                )
            finally:
                await state.finish()

    except Exception as e:
        logging.error(f"Unexpected error in submit_load: {e}")
        await message.answer(
            'Произошла неожиданная ошибка. Попробуйте еще раз.',
            reply_markup=buttons.start
        )
        await state.finish()


def register_handlers_store(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm_store, Text(equals='отмена', ignore_case=True), state='*')
    dp.register_message_handler(start_fsm_store, commands=['store'])
    dp.register_message_handler(name_load, state=StoreFSM.name_product)
    dp.register_message_handler(size_load, state=StoreFSM.size)
    dp.register_message_handler(price_load, state=StoreFSM.price)
    dp.register_message_handler(category_load, state=StoreFSM.category)
    dp.register_message_handler(info_load, state=StoreFSM.info_product)
    dp.register_message_handler(product_id_load, state=StoreFSM.products_id)
    dp.register_message_handler(photo_load, state=StoreFSM.photo, content_types=['photo'])
    dp.register_message_handler(submit_load, state=StoreFSM.submit)