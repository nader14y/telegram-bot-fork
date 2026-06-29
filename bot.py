import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import os

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer("سلام 👋\nپیامتو بنویس، کاملاً ناشناس می‌رسه 💬")

@dp.message()
async def feedback(message: types.Message):

    user_id = message.from_user.id
    username = message.from_user.username
    text = message.text

    await bot.send_message(
        ADMIN_ID,
        f"📩 پیام ناشناس:\n\n{text}\n\n🆔 ID: {user_id}\n👤 Username: @{username if username else 'ندارد'}"
    )
    with open("messages.txt", "a", encoding="utf-8") as f:
        f.write(f"Message: {text}\nID: {user_id}\nUsername: @{username}\n---\n")
        
    await message.answer("ارسال شد 👌")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())