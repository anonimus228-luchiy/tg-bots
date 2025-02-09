from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

cancel_button = KeyboardButton(text='Cancel')

# Категории товаров
categories = ['Одежда', 'Обувь', 'Аксессуары']
category_buttons = [KeyboardButton(text=category) for category in categories]
category_kb = ReplyKeyboardMarkup(
    keyboard=[category_buttons, [cancel_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Размеры
sizes = ['XS', 'S', 'M', 'L', 'XL', 'XXL']
size_buttons = [KeyboardButton(text=size) for size in sizes]
size_kb = ReplyKeyboardMarkup(
    keyboard=[size_buttons, [cancel_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)

# Базовая клавиатура с кнопкой отмены
cancel_kb = ReplyKeyboardMarkup(
    keyboard=[[cancel_button]],
    resize_keyboard=True,
    one_time_keyboard=True
)