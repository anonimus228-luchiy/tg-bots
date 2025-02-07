from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from decouple import config
import random
from config import bot, dp


quiz_data = [
    {
        "question": "Умеешь ли ты программировать?",
        "answers": ["Да", "Нет", "Может быть"],
        "correct": 0,
    },
    {
        "question": "Какой язык используется в Aiogram?",
        "answers": ["Python", "JavaScript", "C++"],
        "correct": 0,
    },
    {
        "question": "Что делает Aiogram?",
        "answers": ["Создает сайты", "Работает с Telegram Bot API", "Запускает игры"],
        "correct": 1,
    }
]


async def start_quiz(message: types.Message):
    await send_quiz(message.from_user.id, 0)


async def send_quiz(chat_id, question_index):
    if question_index >= len(quiz_data):
        await bot.send_message(chat_id, "Викторина завершена! 🎉")
        return

    question = quiz_data[question_index]

    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Далее", callback_data=f"next_{question_index + 1}"))

    await bot.send_poll(
        chat_id=chat_id,
        question=question["question"],
        options=question["answers"],
        is_anonymous=False,
        type='quiz',
        correct_option_id=question["correct"],
        explanation="Ответ в подсказке!",
        reply_markup=keyboard
    )


@dp.callback_query_handler(lambda call: call.data.startswith("next_"))
async def next_question(call: types.CallbackQuery):
    question_index = int(call.data.split("_")[1])
    await send_quiz(call.message.chat.id, question_index)
    await call.answer()


@dp.message_handler(commands=['dice'])
async def roll_dice(message: types.Message):
    await message.answer("Бросаем кость... 🎲")
    await bot.send_dice(message.chat.id, emoji="🎲")


games = ["⚽", "🎰", "🏀", "🎯", "🎳", "🎲"]


@dp.message_handler(lambda message: "game" in message.text.lower())
async def send_game(message: types.Message):
    game = random.choice(games)
    await bot.send_dice(message.chat.id, emoji=game)


@dp.message_handler(commands=['play'])
async def play_game(message: types.Message):
    await message.answer("Ты бросаешь кость... 🎲")
    user_dice = await bot.send_dice(message.chat.id, emoji="🎲")

    await message.answer("Теперь бросает бот... 🎲")
    bot_dice = await bot.send_dice(message.chat.id, emoji="🎲")

    await bot.send_message(
        message.chat.id,
        determine_winner(user_dice.dice.value, bot_dice.dice.value)
    )


def determine_winner(user_score, bot_score):
    if user_score > bot_score:
        return "Ты победил! 🏆"
    elif user_score < bot_score:
        return "Бот победил! 🤖"
    else:
        return "Ничья! 🔥"


async def echo_handler(message: types.Message):
    await message.answer(message.text)


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(echo_handler)
    dp.register_message_handler(start_quiz, commands=['quiz'])
    dp.register_message_handler(roll_dice, commands=['dice'])
    dp.register_message_handler(send_game, lambda message: "game" in message.text.lower())
    dp.register_message_handler(play_game, commands=['play'])
    dp.register_callback_query_handler(next_question, lambda call: call.data.startswith("next_"))




