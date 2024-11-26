from handlers.start import Message, FSMContext, ReplyKeyboardRemove
from keyboards.for_contacts import get_kb_contacts
from keyboards.no_teacher import kb_no_teacher
from aiogram import Router, F
from models.find_teacher import find_teacher_by_full_name
from handlers.class_state import MainStates
from handlers.dict import *


router = Router()


@router.message(F.text == "Я знаю преподавателя")
async def i_know_teacher(message: Message, state: FSMContext):
    await message.answer("Введите ФИО преподавателя", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_group1)


@router.message(F.text == "Ввести ФИО преподавателя")
async def write_name(message: Message, state: FSMContext):
    data_name_to_search[message.chat.id] = message.text
    await state.set_state(MainStates.waiting_for_group1)


@router.message(MainStates.waiting_for_group1)
async def search_by_name(message: Message, state: FSMContext):
    data_name_to_search[message.chat.id] = message.text
    results = find_teacher_by_full_name(message.text.strip())
    await state.clear()
    st = []
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st.append(cleaned_row1)
    else:
        await message.answer(f'Такого преподавателя нет, выберите действие', reply_markup=kb_no_teacher())
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        await message.answer(f'Нашелся преподаватель: {st[0]}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())



@router.message(MainStates.waiting_full_name)
async def search_by_full_name(message: Message, state: FSMContext):
    data_name_to_search[message.chat.id] = message.text
    results = find_teacher_by_full_name(data_name_to_search[message.chat.id])
    st = ""
    await state.clear()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += cleaned_row1
    else:
        await message.answer(f'Такого преподавателя нет, пожалуйста, попробуйте еще раз')
        await state.set_state(MainStates.waiting_full_name)
    if len(results) >= 2:
        await message.answer(f'Нашлось больше 1 преподавателя.\n{", ".join(st)}\nВведите полное имя преподавателя')
        await state.set_state(MainStates.waiting_full_name)
    elif len(results) == 1:
        await message.answer(f'Нашелся преподаватель: {st}')
        await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())
        data_name_to_search[message.chat.id] = st


@router.message(F.text == "Не тот преподаватель")
async def wrong_teacher(message: Message, state: FSMContext):
    await message.answer("Введите ФИО преподавателя", reply_markup=ReplyKeyboardRemove())
    await state.set_state(MainStates.waiting_for_group1)




