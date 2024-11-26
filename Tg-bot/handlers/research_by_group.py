from handlers.start import Message, FSMContext, ReplyKeyboardRemove
from keyboards.for_contacts import get_kb_contacts
from aiogram import Router, F
from handlers.class_state import MainStates
from models.find_teacher import *
from handlers.dict import *
from keyboards.for_fil_dep import get_fil_dep


router = Router()


@router.message(F.text == "Поиск по группе")
async def search_by_group(message: Message, state: FSMContext):
    await message.answer("Введите группу", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_group_teacher)


@router.message(MainStates.waiting_for_group_teacher)
async def search_by_group1(message: Message, state: FSMContext):
    await message.answer(f'Группа для поиска - {message.text}.')
    await state.clear()
    data_group_teacher[message.chat.id] = message.text
    group_to_search = message.text
    results = find_by_group(group_to_search)
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
        await message.answer(f'Нашелся преподаватель: {st}', reply_markup=get_fil_dep())
    else:
        await message.answer(f'Группа введена неверно, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_group_teacher)


@router.message(F.text == "Сделать фильтрацию по кафедре📚")
async def search_by_department_and_group(message: Message, state: FSMContext):
    await message.answer(f'Введите номер кафедры', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_g_teacher)


@router.message(MainStates.waiting_for_g_teacher)
async def search_by_department_and_group1(message: Message, state: FSMContext):
    group_to_search = data_group_teacher.get(message.chat.id)
    data_dep_u[message.chat.id] = message.text
    dep_to_search = data_dep_u.get(message.chat.id)
    data_dep_to_search[message.chat.id] = dep_to_search
    data_group_to_search[message.chat.id] = group_to_search
    results = find_teacher_by_group_and_department(dep_to_search, group_to_search)
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Кафедра введена неверно, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_g_teacher)
    if len(results) >= 2:
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Введите ФИО преподавателя', reply_markup=ReplyKeyboardRemove())
        await state.set_state(MainStates.waiting_for_name4)
    elif len(results) == 1:
        await message.answer(f'Нашелся преподаватель: {st}')
        data_name_to_search[message.chat.id] = st
        await message.answer(f'Выберите действие', reply_markup = get_kb_contacts())


@router.message(MainStates.waiting_for_name4)
async def search_by_department_and_group_and_full_name(message: Message, state: FSMContext):
    name_to_search = message.text
    data_name_to_search[message.chat.id] = message.text
    await state.clear()
    results = find_by_department_and_group_and_full_name(name_to_search, data_dep_to_search.get(message.chat.id), data_group_to_search.get(message.chat.id))
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Такого преподавателя не найдено, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_name4)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())


@router.message(F.text == "Сделать фильтрацию по предмету📚")
async def search_by_subject_and_group(message: Message, state: FSMContext):
    await message.answer(f'Введите название предмета', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_sub_teacher)


@router.message(MainStates.waiting_for_sub_teacher)
async def search_by_subject_and_group1(message: Message, state: FSMContext):
    group_to_search = data_group_teacher.get(message.chat.id)
    data_sub_u[message.chat.id] = message.text
    sub_to_search = data_sub_u.get(message.chat.id)
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
        await message.answer(f'Предмет не найден, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_sub_teacher)
    if len(results) >= 2:
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Введите ФИО преподавателя', reply_markup=ReplyKeyboardRemove())
        await state.set_state(MainStates.waiting_for_name5)
    elif len(results) == 1:
        await message.answer(f'Нашелся преподаватель: {st}')
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Выберите действие', reply_markup = get_kb_contacts())


@router.message(MainStates.waiting_for_name5)
async def search_by_subject_and_group_and_name(message: Message, state: FSMContext):
    name_to_search = message.text
    data_name_to_search[message.chat.id] = message.text
    await state.clear()
    results = find_by_subject_and_group_and_name(name_to_search,data_group_to_search.get(message.chat.id),data_sub_to_search.get(message.chat.id))
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Такого преподавателя не найдено, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_name5)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())


@router.message(F.text == "Ввести ФИО преподавателя из списка📚")
async def search_by_name_and_group(message: Message, state: FSMContext):
    await message.answer(f'Введите ФИО преподавателя', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_name_teacher)


@router.message(MainStates.waiting_name_teacher)
async def search_by_name_and_group1(message: Message, state: FSMContext):
    data_name_to_search[message.chat.id] = message.text
    group_to_search = data_group_teacher.get(message.chat.id)
    name_to_search = message.text
    results = find_by_name_and_group(name_to_search, group_to_search)
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Преподаватель не найден, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_name_teacher)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())


