from aiogram import types, Router, F
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from kbds import kbds
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
    await message.answer("Привет, я виртуальный помощник, я помогу тебе посчитать зарплату", reply_markup=kbds.start_kb)


@user_router.message(F.text == "Посчитать зарплату")
async def count_salary(message: types.Message):
    await message.answer("Хотите ввести всю сумму или посчитать для вас?", reply_markup=kbds.start_kb2)
    
    
@user_router.message(StateFilter(None), F.text == "Ввести всю выручку за месяц")
async def how_many_days(message: types.Message, state: FSMContext):
    if not str(message.text).isdigit():
        await message.answer(
            "Сколько смен у Вас было в месяце?", reply_markup=kbds.start_kb3)
        await state.set_state(CountSalaryAll.days)
        return
    await message.answer("Упс, что-то пошло не так, введите количество отработанных смен", reply_markup=kbds.start_kb3)
    

@user_router.message(StateFilter('*'), F.text.casefold() == "вернуться в начало")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Хотите ввести всю сумму или посчитать для вас?", reply_markup=kbds.start_kb2)
    

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
            await message.answer(f"Ок, вы вернулись к предыдущему шагу\n{CountSalaryAll.state_dict[previous.state]}")
            return
        previous = step


@user_router.message(CountSalaryAll.days, F.text) 
async def how_many_sum(message: types.Message, state: FSMContext):
    if str(message.text).isdigit(): 
        await state.update_data(days=message.text)
        await message.answer("Введите всю выручку за отработанные дни", reply_markup=kbds.start_kb3)
        await state.set_state(CountSalaryAll.summ)
        return
    await message.answer("Упс, что-то пошло не так, введите количество отработанных смен", reply_markup=kbds.start_kb3)


@user_router.message(CountSalaryAll.days) 
async def how_many_sum(message: types.Message):
    await message.answer("Упс, что-то пошло не так, введите выручку за отработанные дни", reply_markup=kbds.start_kb3)


@user_router.message(CountSalaryAll.summ, F.text)
async def service(message: types.Message, state: FSMContext):
    if str(message.text).isdigit():
        await state.update_data(summ=message.text)
        await message.answer("Вы прошли сервис в этом месяце 'Да/Нет'", reply_markup=kbds.start_kb3)
        await state.set_state(CountSalaryAll.service)
        return
    await message.answer("Упс, что-то пошло не так, введите выручку за отработанные дни", reply_markup=kbds.start_kb3)


@user_router.message(CountSalaryAll.summ)
async def salary(message: types.Message):
    await message.answer("Упс, что-то пошло не так, введите выручку за отработанные дни", reply_markup=kbds.start_kb3)


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
    await message.answer("Упс, что-то пошло не так, ответьте, вы прошли сервис 'Да/Нет'", reply_markup=kbds.start_kb3)
    

@user_router.message(CountSalaryAll.service)
async def done(message: types.Message):
    await message.answer("Упс, что-то пошло не так, ответьте, вы прошли сервис 'Да/Нет'", reply_markup=kbds.start_kb3)



###################################################################################################

class CountSalaryEvery(StatesGroup):
    days_every = State()
    summ_every = State()
    service_every = State()


@user_router.message(StateFilter(None), F.text == "Посчитать за каждый день")
async def how_many_days(message: types.Message, state: FSMContext):
    await message.answer("Сколько смен у Вас было в месяце?", reply_markup=kbds.start_kb4)
    await state.set_state(CountSalaryEvery.days_every)


@user_router.message(StateFilter('*'), F.text.casefold() == "вернуться в начало")
async def cancel_handler(message: types.Message, state: FSMContext) -> None:

    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Хотите ввести всю сумму или посчитать для вас?", reply_markup=kbds.start_kb2)


@user_router.message(CountSalaryEvery.days_every, F.text)
async def how_many_sum(message: types.Message, state: FSMContext):
    await state.update_data(days=message.text)
    await message.answer(f"Введите выручку за 1-ый день", reply_markup=kbds.start_kb4)
    await state.set_state(CountSalaryEvery.summ_every)


@user_router.message(CountSalaryEvery.summ_every, F.text)
async def how_many_sum(message: types.Message, state: FSMContext):
    await state.update_data(summ_every=message.text)
    data = await state.get_data()
    count_summ = data.get('count_summ', 0)
    await state.update_data(count_summ = count_summ + int(message.text))
    print(count_summ)
    days = int(data['days'])
    current_day = data.get('current_day', 2)  # Получаем текущий день из состояния, если он есть
    if current_day <= days:
        await message.answer(f"Введите выручку за {current_day}-ый день", 
                            reply_markup=kbds.start_kb4)
        await state.update_data(current_day=current_day + 1)  # Увеличиваем счетчик дня
        await state.set_state(CountSalaryEvery.summ_every)
    else:
        await message.answer("Вы прошли сервис в этом месяце 'Да/Нет'", reply_markup=kbds.start_kb4)
        await state.set_state(CountSalaryEvery.service_every)


@user_router.message(CountSalaryEvery.service_every, F.text)
async def every_service(message: types.Message, state: FSMContext):
    await state.update_data(service_every=message.text)
    data = await state.get_data()
    await message.answer(f"Вашу зарплата без учета НДФЛ составит примерно: {ct.count_every(data)}р.", reply_markup=kbds.del_kb)
    await state.clear()