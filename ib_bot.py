import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import OpenAI

# 🔑 Переменные окружения (Railway)
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # сюда sk-or-v1...

# Проверка
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден!")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY не найден!")

# 🤖 Инициализация
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# ⚡ ВАЖНО: base_url для OpenRouter
client = OpenAI(
    api_key=OPENAI_API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

# 📌 /start
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(
        "👋 Привет!\n"
        "Я бот по информационной безопасности.\n\n"
        "Задай любой вопрос 👇"
    )

# 🧠 Основная логика
@dp.message()
async def handle_question(message: types.Message):
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",  # бесплатная модель
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
        await message.answer("⚠️ Ошибка при обработке запроса")

# 🚀 Запуск
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
