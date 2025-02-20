# from handlers import echo, quiz
# import commands
# from aiogram import executor
# import logging
# from config import Admins, bot, dp
#
# async def on_startup(_):
#     if Admins:
#         for admin in Admins:
#             try:
#                 await bot.send_message(chat_id=admin, text='Бот включен!')
#             except Exception as e:
#                 logging.error(f"Не удалось отправить сообщение админу {admin}: {e}")
#     logging.info("Бот успешно запущен!")
#
# async def on_shutdown(_):
#     if Admins:
#         for admin in Admins:
#             try:
#                 await bot.send_message(chat_id=admin, text='Бот выключен!')
#             except Exception as e:
#                 logging.error(f"Не удалось отправить сообщение админу {admin}: {e}")
#     logging.info("Бот завершает работу!")
#
# def register_all_handlers():
#     commands.register_handlers(dp)
#     quiz.register_handlers(dp)
#     echo.register_handlers(dp)
#
# if __name__ == '__main__':
#     logging.basicConfig(level=logging.INFO)
#     register_all_handlers()
#     executor.start_polling(dp, skip_updates=True,
#                          on_startup=on_startup,
#                          on_shutdown=on_shutdown)