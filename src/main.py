import asyncio
import os

from aiogram import Bot, Dispatcher, types
from dotenv import find_dotenv, load_dotenv
load_dotenv(find_dotenv())

from handlers.user_private import user_router

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(user_router)


async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

asyncio.run(main())

