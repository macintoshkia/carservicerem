import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from sms_sender import send_sms
from db import init_db, add_user, get_due_services
from datetime import datetime, timedelta

TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("سلام! لطفاً اطلاعات زیر را برای ثبت خودرو ارسال کنید:

"
                         "فرمت:
نام مالک
نام خودرو
شماره پلاک
شماره تماس
کیلومتر فعلی
تاریخ آخرین سرویس (YYYY-MM-DD)")

@dp.message()
async def collect_info(message: types.Message):
    try:
        name, car, plate, phone, km, last_service = message.text.split('\n')
        add_user(name, car, plate, phone, int(km), last_service, message.chat.id)
        await message.answer("اطلاعات با موفقیت ذخیره شد.")
    except Exception as e:
        await message.answer("خطا در دریافت اطلاعات. لطفاً فرمت را بررسی کنید.")

async def daily_check():
    while True:
        due = get_due_services()
        for user in due:
            text = f"یادآوری سرویس:\n{user['name']} عزیز، زمان سرویس خودروی {user['car']} با پلاک {user['plate']} فرا رسیده است."
            await bot.send_message(chat_id=user['chat_id'], text=text)
            send_sms(user['phone'], text)
        await asyncio.sleep(86400)

async def main():
    init_db()
    asyncio.create_task(daily_check())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())