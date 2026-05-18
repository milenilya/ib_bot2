import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI

# 🔑 Переменные окружения (Railway Variables)
BOT_TOKEN = os.getenv("8875791086:AAE6OTcWse3NKGP245ggVU625KUPv6ohCOk")
OPENAI_API_KEY = os.getenv("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")

# Проверка ключей
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден!")

# Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = OpenAI(api_key=OPENAI_API_KEY)

# 📌 /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n"
        "Я бот по информационной безопасности.\n\n"
        "📌 Команды:\n"
        "/help — помощь\n"
        "/question — задать вопрос"
    )

# 📌 /help
@dp.message(Command("help"))
async def help_cmd(message: types.Message):
    await message.answer(
        "📌 Доступные команды:\n\n"
        "/start — запуск\n"
        "/help — помощь\n"
        "/question — задать вопрос"
    )

# 📌 /question
@dp.message(Command("question"))
async def question_cmd(message: types.Message):
    await message.answer("✍️ Напиши свой вопрос следующим сообщением.")

# 🧠 Обработка сообщений
@dp.message()
async def handle_question(message: types.Message):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Ты эксперт по информационной безопасности. Отвечай кратко и понятно."},
                {"role": "user", "content": message.text}
            ]
        )

        answer = response.choices[0].message.content

        if not answer:
            answer = "Не удалось получить ответ 😢"

        await message.answer(answer)

    except Exception as e:
        print("ОШИБКА:", e)
        await message.answer("⚠️ Ошибка при обработке запроса. Проверь логи.")

# 🚀 Запуск
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
