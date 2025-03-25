import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta

API_TOKEN = "7713036557:AAEIooFI191wMaYZL9_Bm53x5ew6kXljT4Q"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
scheduler = AsyncIOScheduler()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для 31-дневного вызова 💪")

async def scheduled_message(chat_id: int, text: str):
    await bot.send_message(chat_id=chat_id, text=text)

def schedule_daily_message(chat_id: int, text: str, hour: int = 9, minute: int = 0):
    job_id = f"daily_message_{chat_id}"
    scheduler.add_job(
        scheduled_message,
        trigger='cron',
        hour=hour,
        minute=minute,
        args=[chat_id, text],
        id=job_id,
        replace_existing=True,
    )

@dp.message_handler(commands=['challenge'])
async def challenge_handler(message: types.Message):
    chat_id = message.chat.id
    text = "Держи ежедневное напоминание! Начинаем с завтрашнего дня 🚀"
    await message.answer(text)
    schedule_daily_message(chat_id, "Не забывай про свой челлендж! 🔥", hour=9, minute=0)

async def on_startup(dispatcher):
    scheduler.start()
    logging.info("Scheduler started.")

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(on_startup(dp))
    executor.start_polling(dp, skip_updates=True)
