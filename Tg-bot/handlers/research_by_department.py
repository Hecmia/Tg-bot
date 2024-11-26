from handlers.start import Message, FSMContext, ReplyKeyboardRemove
from keyboards.for_contacts import get_kb_contacts
from aiogram import Router, F
from handlers.class_state import MainStates
from keyboards.for_fil_group import get_fil_group
from models.find_teacher import *
from handlers.dict import *
from keyboards.for_fil_dep import get_fil_dep


router = Router()



@router.message(F.text == "Поиск по кафедре")
async def search_by_department(message: Message, state: FSMContext):
    await message.answer("Введите кафедру преподавателя", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_dep)


@router.message(MainStates.waiting_for_dep)
async def search_by_department1(message: Message, state: FSMContext):
    await message.answer(f'Кафедра для поиска - {message.text}.')
    data_dep_dep[message.chat.id] = ("Кафедра " + message.text)
    data_dep_to_search[message.chat.id] = data_dep_dep[message.chat.id]
    await state.clear()
    dep_to_search = "Кафедра " + message.text
    results = find_teacher_by_department(dep_to_search)
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
        await message.answer(f'Нашелся преподаватель: {st}', reply_markup=get_fil_group())
    else:
        await message.answer(f'Кафедра введена неправильно, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_for_dep)


@router.message(F.text == "Сделать фильтрацию по группе🏫")
async def search_by_group_and_department(message: Message, state: FSMContext):
    await message.answer(f'Введите номер группы', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_gr_teacher)


@router.message(MainStates.waiting_gr_teacher)
async def search_by_group_and_department1(message: Message, state: FSMContext):
    dep_to_search = data_dep_dep.get(message.chat.id)
    group_to_search = message.text
    data_group_to_search[message.chat.id] = group_to_search
    data_dep_to_search[message.chat.id] = dep_to_search
    results = find_teacher_by_group_and_department(dep_to_search, group_to_search)
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'На этой кафедре никто не ведет эту группу, пожалуйста, поменяйте номер группы')
        await state.set_state(MainStates.waiting_gr_teacher)

    if len(results) >= 2:
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Введите ФИО преподавателя', reply_markup=ReplyKeyboardRemove())
        await state.set_state(MainStates.waiting_for_name1)

    elif len(results) == 1:
        await message.answer(f'Нашелся преподаватель: {st}')
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Выберите действие', reply_markup=get_kb_contacts())


@router.message(MainStates.waiting_for_name1)
async def search_by_name_and_department(message: Message, state: FSMContext):
    name_to_search = message.text
    data_name_to_search[message.chat.id] = message.text
    await state.clear()
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ? AND department LIKE ?',
                   (f'%{name_to_search}%',f'%{data_dep_to_search.get(message.chat.id)}%',))
    results = cursor.fetchall()
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Неправильно введено ФИО, пожалуйста, введите его снова')
        await state.set_state(MainStates.waiting_for_name1)


    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())


@router.message(F.text == "Ввести ФИО преподавателя из списка🏫")
async def search_by_name_and_department(message: Message, state: FSMContext):
    await message.answer(f'Введите ФИО преподавателя', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_name_teacher1)


@router.message(MainStates.waiting_name_teacher1)
async def search_by_name_and_department1(message: Message, state: FSMContext):
    data_name_to_search[message.chat.id] = message.text
    dep_to_search = data_dep_dep.get(message.chat.id)
    name_to_search = message.text
    results = find_by_name_and_department(name_to_search, dep_to_search)
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Такого преподавателя не найдено, введите имя еще раз')
        await state.set_state(MainStates.waiting_name_teacher1)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())


@router.message(F.text == "Сделать фильтрацию по предмету🏫")
async def search_by_department_and_subject(message: Message, state: FSMContext):
    await message.answer(f'Введите название предмета', reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_sub_sub)


@router.message(MainStates.waiting_for_sub_sub)
async def search_by_department_and_subject1(message: Message, state: FSMContext):
    dep_to_search = data_dep_dep.get(message.chat.id)
    sub_to_search = message.text
    data_dep_to_search[message.chat.id] = dep_to_search
    data_sub_to_search[message.chat.id] = sub_to_search
    results = find_by_department_and_subject(dep_to_search, sub_to_search)
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Предмет введен неверно, пожалуйста, попробуйте снова')
        await state.set_state(MainStates.waiting_for_sub_sub)
    if len(results) >= 2:
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Введите ФИО преподавателя', reply_markup=ReplyKeyboardRemove())
        await state.set_state(MainStates.waiting_for_name2)
    elif len(results) == 1:
        await message.answer(f'Нашелся преподаватель: {st}')
        data_name_to_search[message.chat.id] = st
        await message.answer(f'Выберите действие', reply_markup=get_kb_contacts())


@router.message(MainStates.waiting_for_name2)
async def search_by_department_name_subject(message: Message, state: FSMContext):
    name_to_search = message.text
    data_name_to_search[message.chat.id] = message.text
    await state.clear()
    results = find_by_department_name_subject(name_to_search, data_dep_to_search.get(message.chat.id), data_sub_to_search.get(message.chat.id))
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'ФИО преподавателя введено неправильно, пожалуйста, попробуйте снова')
        await state.set_state(MainStates.waiting_for_name2)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        data_name_to_search[message.chat.id] = st.strip()
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())