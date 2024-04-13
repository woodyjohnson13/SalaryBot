from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

start_kb = ReplyKeyboardBuilder()
start_kb.add(
    KeyboardButton(text="Посчитать зарплату")
)
start_kb.adjust(1)


start_kb2 = ReplyKeyboardBuilder()
start_kb2.add(
    KeyboardButton(text="Ввести всю выручку за месяц?"),
    KeyboardButton(text="Посчитать за каждый день")
)
start_kb2.adjust(2)




start_kb3 = ReplyKeyboardBuilder()
start_kb3.add(
    KeyboardButton(text="Вернуться в начало"),
    KeyboardButton(text="Вернуться на один шаг")
)
start_kb3.adjust(2)


start_kb4 = ReplyKeyboardBuilder()
start_kb4.add(
    KeyboardButton(text="Вернуться в начало")
)
start_kb4.adjust(1)

