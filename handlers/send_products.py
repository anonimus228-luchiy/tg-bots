from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db.main_db import fetch_products_paginated, fetch_all_products

async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    button_all = types.InlineKeyboardButton('Вывести все товары', callback_data='send_all')
    button_one = types.InlineKeyboardButton("Вывести по одному", callback_data='send_one_0')
    keyboard.add(button_all, button_one)
    await message.answer('Выберите как просмотреть товары:', reply_markup=keyboard)

async def send_all_products(call: types.CallbackQuery):
    products = fetch_all_products()
    if products:
        for product in products:
            caption = (f'Название товара - {product["name_product"]}\n'
                       f'Размер товара - {product["size"]}\n'
                       f'Категория - {product["category"]}\n'
                       f'Артикул - {product["product_id"]}\n'
                       f'Инфо - {product["info_product"]}\n'
                       f'Цена - {product["price"]}')
            await call.message.answer_photo(photo=product["photo"], caption=caption)
    else:
        await call.message.answer('База пуста! Товаров нет.')

async def send_one_product(call: types.CallbackQuery):
    _, page = call.data.split('_')
    page = int(page)
    products, has_more = fetch_products_paginated(page)
    if products:
        product = products[0]
        caption = (f'Название товара - {product["name_product"]}\n'
                   f'Размер товара - {product["size"]}\n'
                   f'Категория - {product["category"]}\n'
                   f'Артикул - {product["product_id"]}\n'
                   f'Инфо - {product["info_product"]}\n'
                   f'Цена - {product["price"]}')
        keyboard = types.InlineKeyboardMarkup()
        if has_more:
            next_button = types.InlineKeyboardButton("Далее", callback_data=f'send_one_{page + 1}')
            keyboard.add(next_button)
        await call.message.answer_photo(photo=product["photo"], caption=caption, reply_markup=keyboard)
    else:
        await call.message.answer('Товары закончились!')

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands='send_products')
    dp.register_callback_query_handler(send_all_products, Text(equals='send_all'))
    dp.register_callback_query_handler(send_one_product, Text(startswith='send_one_'))
