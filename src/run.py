import asyncio
import os

from aiogram import Bot, Dispatcher, types
from commands.bot_cmd_list import private
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


from handlers.user_private import user_router

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()
dp.include_router(user_router)


async def main() -> None:
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats())
    await bot.delete_webhook(drop_pending_updates=True)#сбрасываем сообщения от пользователей перед запуском
    await dp.start_polling(bot)#запуск бота

asyncio.run(main())

