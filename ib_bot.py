import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI

# 🔑 Берем ключи из переменных окружения
BOT_TOKEN = os.getenv("8875791086:AAE6OTcWse3NKGP245ggVU625KUPv6ohCOk")
OPENAI_API_KEY = os.getenv("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")
BOT_TOKEN = "8875791086:AAE6OTcWse3NKGP245ggVU625KUPv6ohCOk"
OPENAI_API_KEY = "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"

# 🔧 Проверка (чтобы не было тупых ошибок)
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден!")

# 🤖 Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

# 📌 Команда /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n"
        "Я бот по информационной безопасности.\n\n"
        "📌 Команды:\n"
        "/help — список команд\n"
        "/question — задать вопрос"
    )

# 📌 Команда /help
@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📌 Доступные команды:\n\n"
        "/start — запуск бота\n"
        "/help — помощь\n"
        "/question — задать вопрос по инфобезу"
    )

# 📌 Команда /question
@dp.message(Command("question"))
async def question_cmd(message: types.Message):
    await message.answer("✍️ Напиши свой вопрос следующим сообщением.")

# 🧠 Обработка всех сообщений
@dp.message()
async def handle_question(message: types.Message):
    user_question = message.text

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты эксперт по информационной безопасности. Отвечай кратко и понятно."},
                {"role": "user", "content": user_question}
            ]
        )

        answer = response.choices[0].message.content

        await message.answer(answer)

    except Exception as e:
        await message.answer("⚠️ Ошибка при обработке запроса.")
        print("Ошибка:", e)

# 🚀 Запуск бота
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
