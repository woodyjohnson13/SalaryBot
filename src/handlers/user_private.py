from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from kbds.kbds import start_kb, start_kb2, start_kb3
from salary.count_salary import Salary

user_router = Router()

ct = Salary()
class CountSalaryAll(StatesGroup):
    days = State()
    summ = State()
    service = State()

    state_dict = {'CountSalaryAll:days':'Введите количество дней заного',
                  'CountSalaryAll:summ':'Введите всю выручку заного',
                  'CountSalaryAll:service':'Еще раз скажите, прошли сервис "Да/Нет"'}


@user_router.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Привет, я виртуальный помощник, я помогу тебе посчитать зарплату", 
                        reply_markup=start_kb.as_markup(
                           resize_keyboard=True,
                           input_field_placeholder="Выберите нужное действие?" ))


@user_router.message(F.text == "Посчитать зарплату")
async def count_salary(message: types.Message):
    await message.answer("Хотите ввести всю сумму или посчитать для вас?",
                        reply_markup=start_kb2.as_markup(
                           resize_keyboard=True,
                           input_field_placeholder="Выберите нужное действие?" ))
    
    



@user_router.message(StateFilter(None), F.text == "Ввести всю выручку за месяц?")
async def how_many_days(message: types.Message, state: FSMContext):
    if not str(message.text).isdigit():
        await message.answer(
            "Сколько смен у Вас было в месяце?", reply_markup=start_kb3.as_markup(
                resize_keyboard=True,
                input_field_placeholder="Введите количество смен"))
        await state.set_state(CountSalaryAll.days)
        return
    await message.answer("Упс, что-то пошло не так, введите количество отработанных смен", reply_markup=start_kb3.as_markup(
                        resize_keyboard=True,
                        input_field_placeholder="Введите количество смен"))
    



@user_router.message(StateFilter('*'), F.text.casefold() == "вернуться в начало")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Хотите ввести всю сумму или посчитать для вас?",
                        reply_markup=start_kb2.as_markup(
                           resize_keyboard=True,
                           input_field_placeholder="Выберите нужное действие?"))
    

@user_router.message(StateFilter('*'), F.text.casefold() == "вернуться на один шаг")
async def cancel_step_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state == CountSalaryAll.days:
        await message.answer("Предыдущего шага нет, или введите количество дней или напишите 'вернуться в начало'")
        return

    previous = None
    for step in CountSalaryAll.__all_states__:
        if step.state == current_state:
            await state.set_state(previous)
            await message.answer(f"Ок, вы вернулись к предыдущему шагу \n {CountSalaryAll.state_dict[previous.state]}")
            return
        previous = step

@user_router.message(CountSalaryAll.days, F.text) 
async def how_many_sum(message: types.Message, state: FSMContext):
    if str(message.text).isdigit(): 
        await state.update_data(days=message.text)
        await message.answer("Введите всю выручку за отработанные дни", reply_markup=start_kb3.as_markup(
                            resize_keyboard=True,
                            input_field_placeholder="Введите выручку"))
        await state.set_state(CountSalaryAll.summ)
        return
    await message.answer("Упс, что-то пошло не так, введите количество отработанных смен", reply_markup=start_kb3.as_markup(
                        resize_keyboard=True,
                        input_field_placeholder="Введите количество смен"))

@user_router.message(CountSalaryAll.days) 
async def how_many_sum(message: types.Message):
    await message.answer("Упс, что-то пошло не так, введите выручку за отработанные дни", reply_markup=start_kb3.as_markup(
                        resize_keyboard=True,
                        input_field_placeholder="Введите выручку"))



@user_router.message(CountSalaryAll.summ, F.text)
async def salary(message: types.Message, state: FSMContext):
    if str(message.text).isdigit():
        await state.update_data(summ=message.text)
        await message.answer("Вы прошли сервис в этом месяце 'Да/Нет'", reply_markup=start_kb3.as_markup(
                            resize_keyboard=True,
                            input_field_placeholder="Введите выручку"))
        await state.set_state(CountSalaryAll.service)
        return
    await message.answer("Упс, что-то пошло не так, введите выручку за отработанные дни", reply_markup=start_kb3.as_markup(
                        resize_keyboard=True,
                        input_field_placeholder="Введите выручку"))


@user_router.message(CountSalaryAll.summ)
async def salary(message: types.Message):
    await message.answer("Упс, что-то пошло не так, введите выручку за отработанные дни", reply_markup=start_kb3.as_markup(
                        resize_keyboard=True,
                        input_field_placeholder="Введите выручку"))


@user_router.message(CountSalaryAll.service, F.text)
async def done(message: types.Message, state: FSMContext):
    answer_list = ['да', 'нет']
    if str(message.text).lower() in answer_list:
        await state.update_data(service=message.text)
        data = await state.get_data()
        await message.answer(f"Вашу зарплата без учета НДФЛ составит примерно: {ct.count_all(data)}р.",
                            reply_markup=types.ReplyKeyboardRemove())
        await state.clear()
        return
    await message.answer("Упс, что-то пошло не так, ответьте, вы прошли сервис 'Да/Нет'", reply_markup=start_kb3.as_markup(
                        resize_keyboard=True,
                        input_field_placeholder="Да/Нет?"))
    

@user_router.message(CountSalaryAll.service)
async def done(message: types.Message):
    await message.answer("Упс, что-то пошло не так, ответьте, вы прошли сервис 'Да/Нет'", reply_markup=start_kb3.as_markup(
                        resize_keyboard=True,
                        input_field_placeholder="Да/Нет?"))



###################################################################################################

class CountSalaryEvery(StatesGroup):
    summ_every = State()
    days_every = State()
    service_every = State()

@user_router.message(StateFilter(None), F.text == "Посчитать за каждый день")
async def how_many_days(message: types.Message, state: FSMContext):
    await message.answer(
        "Сколько смен у Вас было в месяце?", reply_markup=types.ReplyKeyboardRemove()
    )
    await state.set_state(CountSalaryEvery.days_every)

@user_router.message(CountSalaryEvery.days_every, F.text)
async def how_many_sum(message: types.Message, state: FSMContext):
    await state.update_data(days=message.text)
    await message.answer(f"Введите выручку за 1-ый день")
    await state.set_state(CountSalaryEvery.summ_every)
"""
# @user_router.message(CountSalaryEvery.summ, F.text)
# async def how_many_sum(message: types.Message, state: FSMContext):
#     await state.update_data(summ=message.text)
#     data = await state.get_data
#     day = 2
#     if await data[day] <= day:
#         await message.answer(f"Введите выручку за {day} день")
#         await state.set_state(CountSalaryEvery.summ)
#         day += 1
#     else:
#         await message.answer(f"Ваша зарплата составит {data}")
"""  

@user_router.message(CountSalaryEvery.summ_every, F.text)
async def how_many_sum(message: types.Message, state: FSMContext):
    await state.update_data(summ_every=message.text)
    data = await state.get_data()
    print(str(data))
    days = int(data['days'])  # Количество дней, указанных пользователем
    print(str(days))
    current_day = data.get('current_day', 2)  # Получаем текущий день из состояния, если он есть
    print(str(current_day))
    if current_day <= days:
        await message.answer(f"Введите выручку за {current_day}-ый день")
        await state.update_data(current_day=current_day + 1)  # Увеличиваем счетчик дня
        await state.set_state(CountSalaryEvery.summ_every)
    else:
        total_salary = 0
        for day in range(1, current_day):
            total_salary += float(data.get(f"day_{day}_summ", 0))
            print(str(total_salary))
        await message.answer(f"Ваша зарплата за месяц составит: {total_salary}")
        await state.finish()
