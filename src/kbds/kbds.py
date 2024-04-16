from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="Посчитать зарплату")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите нужное действие")


start_kb2 = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text="Ввести всю выручку за месяц"),
        KeyboardButton(text="Посчитать за каждый день")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите нужное действие")


start_kb3 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Вернуться в начало"),
        KeyboardButton(text="Вернуться на один шаг")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Следуйте инструкции")


start_kb4 = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Вернуться в начало")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Следуйте инструкции")

del_kb = ReplyKeyboardRemove()

