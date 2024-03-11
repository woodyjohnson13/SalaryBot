from aiogram import types, Router
from aiogram.filters import CommandStart, Command

user_router = Router()



@user_router.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer("Привет, я виртуальный помощник, я помогу тебе посчитать зарплату")

