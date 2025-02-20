from aiogram.dispatcher.filters.state import State, StatesGroup

class ProductState(StatesGroup):
    name = State()
    category = State()
    photo = State()
    size = State()
    price = State()