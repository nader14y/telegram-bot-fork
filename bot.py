import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

TOKEN = os.getenv("TOKEN") or "Test"
print(TOKEN)
ADMIN_ID = int(os.getenv("ADMIN_ID"))
OFFSET_FILE = os.getenv("OFFSET_FILE", "offset.txt")

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


def load_offset():
    try:
        with open(OFFSET_FILE) as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return None


def save_offset(offset):
    with open(OFFSET_FILE, "w") as f:
        f.write(str(offset))


async def main():
    """Fetch all pending updates once, process them, then exit."""
    offset = load_offset()
    last_update_id = None
    try:
        # timeout=0 -> return immediately with whatever is queued (no long poll)
        updates = await bot.get_updates(offset=offset, timeout=0)
        for update in updates:
            await dp.feed_update(bot, update)
            last_update_id = update.update_id

        if last_update_id is not None:
            next_offset = last_update_id + 1
            save_offset(next_offset)
            # Confirm updates server-side so they're never re-sent,
            # even if the offset file is lost between runs.
            await bot.get_updates(offset=next_offset, timeout=0)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())


