from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

# Reply клавиатура для основного меню
start = ReplyKeyboardMarkup(resize_keyboard=True)
start.add(
    KeyboardButton('/quiz'),
    KeyboardButton('/store'),
    KeyboardButton('/mem')
)

# Inline клавиатура для подтверждения
confirm_keyboard = InlineKeyboardMarkup()
confirm_keyboard.add(
    InlineKeyboardButton('Да ✅', callback_data='confirm'),
    InlineKeyboardButton('Нет ❌', callback_data='cancel')
)

# Клавиатура для отмены операции
cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_keyboard.add(KeyboardButton('/cancel'))

# Кнопки для FSM
cancel_fsm = ReplyKeyboardMarkup(resize_keyboard=True)
cancel_fsm.add(KeyboardButton('отмена'))

# Кнопки подтверждения для FSM
submit = ReplyKeyboardMarkup(resize_keyboard=True)
submit.add(
    KeyboardButton('да'),
    KeyboardButton('нет')
)

# Кнопка для удаления клавиатуры
remove_keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)