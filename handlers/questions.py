from cgitb import handler
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.for_questions import get_kb
from keyboards.for_reviews import get_kb_reviews
from aiogram import Bot, Dispatcher
from keyboards.for_do_you_know_teachers import get_kb_do_you_know_teacher
from keyboards.for_contacts import get_kb_contacts
from keyboards.for_schedule import get_kb_schedule
from aiogram import Bot, Router, Dispatcher, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage

class StudentStates(StatesGroup):
    waiting_for_group = State()

class TeacherStates(StatesGroup):
    waiting_for_group1 = State()

class I_TeacherStates(StatesGroup):
    waiting_for_kaf = State()

dp = Dispatcher(storage=MemoryStorage())



#Подключение бд
import sqlite3
connection = sqlite3.connect('database.db')
cursor = connection.cursor()


data_users_student = {}
data_users_teacher = {}

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Приветствую вас! Это бот создан для удобного нахождения контактов и расписания преподавателей, а также отзывов о них. Выберите интересующий вас раздел!",
        reply_markup=get_kb()
    )

@router.message(F.text == "Я преподаватель")
async def i_teacher(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await message.answer("Введите номер вашей кафедры")
    await state.set_state(I_TeacherStates.waiting_for_kaf)

@router.message(I_TeacherStates.waiting_for_kaf)
async def fun3(message: Message, state: FSMContext):
    data_users_teacher[message.chat.id] = message.text
    await message.answer(f'Отлично, ваша кафедра - {data_users_teacher.get(message.chat.id)}.')
    await state.clear()
    await message.answer(f'Вы знаете преподавателя?', reply_markup = get_kb_do_you_know_teacher())


@router.message(F.text == "Я студент")
async def i_student(message: Message, state: FSMContext):
    chat_id = message.chat.id
    await message.answer("Введите номер вашей группы")
    await state.set_state(StudentStates.waiting_for_group)

@router.message(StudentStates.waiting_for_group)
async def fun1(message: Message, state: FSMContext):
    data_users_student[message.chat.id] = message.text
    await message.answer(f'Отлично, ваша группа - {data_users_student.get(message.chat.id)}.')
    await state.clear()
    await message.answer(f'Вы знаете преподавателя?', reply_markup = get_kb_do_you_know_teacher())

@router.message(F.text == "Книга отзывов тг бот")
async def reviews_bot(message: Message):
    await message.answer("Вы находитесь в блоке отзывов о тг боте")

@router.message(F.text == "Отзывы о преподавателях")
async def reviews_professors(message: Message):
    await message.answer("Вы находитесь в блоке отзывов о преподавателях", reply_markup=get_kb_reviews())

@router.message(F.text == "Добавить новый отзыв")
async def create_professor(message: Message):
    await message.answer("Введите ФИО преподавателя")

@router.message(F.text == "Посмотреть отзывы")
async def view(message: Message):
    await message.answer("Введите ФИО преподавателя")

@router.message(F.text == "Я знаю преподавателя")
async def i_know_teacher(message: Message, state: FSMContext):
    await message.answer("Введите ФИО преподавателя")
    await state.set_state(TeacherStates.waiting_for_group1)

@router.message(TeacherStates.waiting_for_group1)
async def fun2(message: Message, state: FSMContext):
    cursor.execute('SELECT name, subjects, department FROM teachers WHERE name LIKE ?', (f'%{message.text.strip()}%',))
    results = cursor.fetchall()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            cleaned_row3 = row[2].strip()
            await message.answer(f'Нашелся преподаватель: {cleaned_row1}')
            await message.answer(f'Предметы: {cleaned_row2}')
            await message.answer(f'Кафедра: {cleaned_row3}')
    else:
        await message.answer(f'Такого преподавателя нет')
    await state.clear()
    await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())

@router.message(F.text == "Не тот преподаватель")
async def fun4(message: Message, state: FSMContext):
    await message.answer("Введите ФИО преподавателя")
    await state.set_state(TeacherStates.waiting_for_group1)

