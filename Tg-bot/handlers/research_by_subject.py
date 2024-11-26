from handlers.start import Message, FSMContext, ReplyKeyboardRemove
from keyboards.for_contacts import get_kb_contacts
from aiogram import Router, F
from handlers.class_state import MainStates
from models.find_teacher import *
from handlers.dict import *
from keyboards.for_yes_no import get_yes_no_sub
from keyboards.for_filtr_fio import get_filtr_fio


router = Router()


@router.message(F.text == "Поиск по предмету")
async def search_by_subject(message: Message, state: FSMContext):
    await message.answer("Введите предмет, который ведет преподаватель", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_sub)


@router.message(MainStates.waiting_for_sub)
async def approve_subject(message: Message, state: FSMContext):
    data_sub[message.chat.id] = message.text
    await message.answer(f'Вы имеете в виду данный предмет - {data_sub.get(message.chat.id)}?', reply_markup=get_yes_no_sub())
    await state.clear()


@router.message(F.text == "Да, это верный предмет")
async def correct_subject(message: Message, state: FSMContext):
    sub_to_search = data_sub.get(message.chat.id)
    results = find_subject(sub_to_search)
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
        await message.answer(f'Нашелся преподаватель: {st}', reply_markup=get_filtr_fio())
    else:
        await message.answer(f'Никто не ведет данный предмет, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_sub)


@router.message(F.text == "Нет, это неверный предмет")
async def incorrect_sub(message: Message, state: FSMContext):
    await message.answer("Введите предмет, который ведет преподаватель", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_sub)


@router.message(F.text == "Ввести ФИО преподавателя из списка")
async def vvod_name(message: Message, state: FSMContext):
    await message.answer("Введите имя преподавателя", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_name)


@router.message(MainStates.waiting_for_name)
async def search_by_name_and_subject(message: Message, state: FSMContext):
    sub_to_search = data_sub.get(message.chat.id)
    name_to_search = message.text
    results = find_by_name_and_subject(name_to_search, sub_to_search)
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
        data_name_to_search[message.chat.id] = cleaned_row1
    else:
        await message.answer(f'Преподаватель не найден, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_name)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())


@router.message(F.text == "Сделать фильтрацию по группе")
async def search_by_group(message: Message, state: FSMContext):
    await message.answer("Введите вашу группу", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_g)


@router.message(MainStates.waiting_for_g)
async def search_by_group_and_subject(message: Message, state: FSMContext):
    data_group_user[message.chat.id] = message.text
    sub_to_search = data_sub.get(message.chat.id)
    group_to_search = data_group_user.get(message.chat.id)
    data_sub_to_search[message.chat.id] = sub_to_search
    data_group_to_search[message.chat.id] = group_to_search
    results = find_search_by_group_and_subject(group_to_search, sub_to_search)
    await state.clear()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Группа введена неверно, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_g)
    if len(results) >= 2:
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Введите ФИО преподавателя', reply_markup=ReplyKeyboardRemove())
        await state.set_state(MainStates.waiting_for_name3)
    elif len(results) == 1:
        await message.answer(f'Нашелся преподаватель: {st}')
        data_name_to_search[message.chat.id] = cleaned_row1
        await message.answer(f'Выберите действие', reply_markup=get_kb_contacts())


@router.message(MainStates.waiting_for_name3)
async def search_by_full_name_and_subject(message: Message, state: FSMContext):
    name_to_search = message.text
    data_name_to_search[message.chat.id] = message.text
    await state.clear()
    results = find_by_full_name_and_subject(name_to_search,data_group_to_search.get(message.chat.id), data_sub_to_search.get(message.chat.id))
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Преподаватель не найден, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_name3)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())


@router.message(F.text == "Сделать фильтрацию по кафедре")
async def search_by_department(message: Message, state: FSMContext):
    await message.answer("Введите кафедру преподавателя", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_d)


@router.message(MainStates.waiting_for_d)
async def search_by_department_and_subject(message: Message, state: FSMContext):
    data_dep_user[message.chat.id] = message.text
    sub_to_search = data_sub.get(message.chat.id)
    dep_to_search = f'Кафедра {data_dep_user.get(message.chat.id)}'
    results = find_by_department_and_subject(dep_to_search, sub_to_search)
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Кафедра введена неверно, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_d)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        data_name_to_search[message.chat.id] = cleaned_row1
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())