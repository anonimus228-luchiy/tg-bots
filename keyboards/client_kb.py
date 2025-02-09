from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('🛍 Каталог'))
    kb.add(KeyboardButton('🛒 Корзина'))
    kb.add(KeyboardButton('ℹ️ О нас'))
    return kb

def get_categories_kb(categories):
    kb = InlineKeyboardMarkup(row_width=2)
    for category in categories:
        kb.add(InlineKeyboardButton(
            text=category[1],
            callback_data=f'category_{category[0]}'
        ))
    return kb

def get_products_kb(products):
    kb = InlineKeyboardMarkup(row_width=2)
    for product in products:
        kb.add(InlineKeyboardButton(
            text=f"{product[2]} - {product[4]}₽",
            callback_data=f'product_{product[0]}'
        ))
    kb.add(InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_categories'))
    return kb

def get_product_kb(product_id):
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(
        InlineKeyboardButton(text='🛒 В корзину', callback_data=f'add_to_cart_{product_id}'),
        InlineKeyboardButton(text='◀️ Назад', callback_data='back_to_products')
    )
    return kb