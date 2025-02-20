from aiogram import executor
import logging
from handlers import commands, echo, quiz, fsm_reg, store_fsm
from config import dp, Admins, bot
import buttons
from db import main_db

async def on_startup(_):
    try:
        await main_db.create_tables()

        for admin in Admins:
            await bot.send_message(
                chat_id=admin,
                text='Бот запущен и готов к работе!',
                reply_markup=buttons.start
            )
    except Exception as e:
        logging.error(f"Ошибка при запуске: {e}")

async def on_shutdown(_):
    try:
        for admin in Admins:
            await bot.send_message(
                chat_id=admin,
                text='Бот выключен!'
            )
    except Exception as e:
        logging.error(f"Ошибка при выключении: {e}")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    
    # Регистрируем все обработчики
    commands.register_handlers(dp)
    quiz.register_handlers(dp)
    fsm_reg.register_handlers_fsm(dp)
    store_fsm.register_handlers_store(dp)  # Добавили регистрацию store handlers
    echo.register_handlers(dp)  # Echo обработчик всегда последний
    
    # Запускаем бота
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )