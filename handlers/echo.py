from aiogram import types, Dispatcher
import random
from config import bot

# Эмодзи для игр
GAME_EMOJI = ["⚽", "🎰", "🏀", "🎯", "🎳", "🎲"]

async def echo_handler(message: types.Message):
    """
    Эхо-обработчик для всех остальных сообщений
    """
    try:
        # Пробуем преобразовать текст в число и вернуть его квадрат
        number = float(message.text)
        await message.answer(f"{number} в квадрате = {number ** 2}")
    except ValueError:
        # Если не получилось преобразовать в число, отправляем текст обратно
        await message.answer(message.text)
    except Exception as e:
        await message.answer("Произошла ошибка при обработке сообщения.")
        print(f"Error in echo_handler: {e}")

async def dice_handler(message: types.Message):

    try:
        await message.answer("🎲 Бросаем кубик...")
        dice_message = await bot.send_dice(message.chat.id, emoji="🎲")
        dice_value = dice_message.dice.value
        await message.answer(f"Выпало число {dice_value}!")
    except Exception as e:
        await message.answer("Произошла ошибка при броске кубика.")
        print(f"Error in dice_handler: {e}")

async def play_game(message: types.Message):
    """
    Обработчик команды /play - игра с ботом
    """
    try:
        await message.answer("Ты бросаешь кубик... 🎲")
        user_dice = await bot.send_dice(message.chat.id, emoji="🎲")
        user_value = user_dice.dice.value
        
        await message.answer("Бот бросает кубик... 🎲")
        bot_dice = await bot.send_dice(message.chat.id, emoji="🎲")
        bot_value = bot_dice.dice.value
        
        # Определяем победителя
        if user_value > bot_value:
            result = "Ты победил! 🏆"
        elif user_value < bot_value:
            result = "Бот победил! 🤖"
        else:
            result = "Ничья! 🤝"
        
        await message.answer(f"\nТвой бросок: {user_value}\nБросок бота: {bot_value}\n\n{result}")
    except Exception as e:
        await message.answer("Произошла ошибка в игре.")
        print(f"Error in play_game: {e}")

async def random_game(message: types.Message):
    """
    Обработчик для случайной мини-игры
    """
    try:
        game = random.choice(GAME_EMOJI)
        await message.answer(f"Играем в {game}")
        await bot.send_dice(message.chat.id, emoji=game)
    except Exception as e:
        await message.answer("Произошла ошибка при запуске игры.")
        print(f"Error in random_game: {e}")

def register_handlers(dp: Dispatcher):
    """
    Регистрация обработчиков
    """
    # Игровые команды
    dp.register_message_handler(dice_handler, commands=['dice'])
    dp.register_message_handler(play_game, commands=['play'])
    dp.register_message_handler(random_game, lambda msg: msg.text.lower() == 'game')
    
    # Эхо-обработчик должен быть последним
    dp.register_message_handler(echo_handler)