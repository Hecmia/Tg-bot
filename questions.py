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
from keyboards.for_filters import get_kb_poisk
from keyboards.for_grops import get_kb_group
from keyboards.for_yes_no import get_yes_no_sub
from keyboards.for_fil2 import get_filtr_subject
from keyboards.for_fil3 import get_fil_a
from keyboards.for_fil4 import get_fil_c
from keyboards.for_fil5 import get_fil_b

class StudentStates(StatesGroup):
    waiting_for_group = State()

class TeacherStates(StatesGroup):
    waiting_for_group1 = State()

class I_TeacherStates(StatesGroup):
    waiting_for_kaf = State()

class DepartmentStates(StatesGroup):
    waiting_for_dep = State()

class SubStates(StatesGroup):
    waiting_for_sub = State()

class NameStates(StatesGroup):
    waiting_for_name = State()

class DeparStates(StatesGroup):
    waiting_for_depar = State()

class SubGrStates(SubStates):
    waiting_for_g = State()

class SubDepStates(SubStates):
    waiting_for_d = State()

class TeacherGroupStates(StatesGroup):
    waiting_for_group_teacher = State()

class TeacherGStates(StatesGroup):
    waiting_for_g_teacher = State()

class GrSubStates(StatesGroup):
    waiting_for_sub_teacher = State()

class TeacherGrStates(StatesGroup):
    waiting_name_teacher = State()

class DepGrStates(StatesGroup):
    waiting_gr_teacher = State()

class DepNameStates(StatesGroup):
    waiting_name_teacher = State()

class TeacherSubSubStates(StatesGroup):
    waiting_for_sub_sub= State()

class TeacherName1States(StatesGroup):
    waiting_for_name1 = State()

class TeacherName2States(StatesGroup):
    waiting_for_name2 = State()

class TeacherName3States(StatesGroup):
    waiting_for_name3 = State()

class TeacherName4States(StatesGroup):
    waiting_for_name4 = State()

class TeacherName5States(StatesGroup):
    waiting_for_name5 = State()

class TeacherName6States(StatesGroup):
    waiting_for_name6 = State()

dp = Dispatcher(storage=MemoryStorage())

#Подключение бд
import sqlite3
connection = sqlite3.connect('database.db')
cursor = connection.cursor()



data_dep_dep = {}
data_sub_u = {}
data_dep_user = {}
data_name_teacher = {}
data_sub = {}
data_users_student = {}
data_users_teacher = {}
data_group_user = {}
data_group_teacher = {}
data_dep_u = {}
data_name_to_search = {}

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

@router.message(F.text == "Я не знаю преподавателя")
async def i_know_teacher(message: Message):
    await message.answer("Выберите фильтр для поиска", reply_markup=get_kb_poisk())

@router.message(TeacherStates.waiting_for_group1)
async def fun2(message: Message, state: FSMContext):
    data_name_to_search[message.chat.id] = message.text
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ?', (f'%{message.text.strip()}%',))
    results = cursor.fetchall()
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            await message.answer(f'Нашелся преподаватель: {cleaned_row1}; {cleaned_row2}')
    else:
        await message.answer(f'Такого преподавателя нет')
    await state.clear()
    await message.answer(f'Что вы хотите узнать?', reply_markup=get_kb_contacts())

@router.message(F.text == "Не тот преподаватель")
async def fun4(message: Message, state: FSMContext):
    await message.answer("Введите ФИО преподавателя")
    await state.set_state(TeacherStates.waiting_for_group1)

@router.message(F.text == "Поиск по кафедре")
async def reviews_bot(message: Message, state: FSMContext):
    await message.answer("Введите кафедру преподавателя")
    await state.set_state(DepartmentStates.waiting_for_dep)

@router.message(DepartmentStates.waiting_for_dep)
async def fun5(message: Message, state: FSMContext):
    await message.answer(f'Кафедра для поиска - {message.text}.')
    data_dep_dep[message.chat.id] = ("Кафедра " + message.text)
    await state.clear()
    dep_to_search = "Кафедра " + message.text
    cursor.execute('SELECT name FROM teachers WHERE department LIKE ?', (f'%{dep_to_search}%',))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'На этой кафедре пусто')
    await message.answer(f'Нашелся преподаватель: {st}', reply_markup = get_fil_b())

@router.message(F.text == "Сделать фильтрацию по группе💜")
async def fun15(message: Message, state: FSMContext):
    await message.answer(f'Введите номер группы')
    await state.set_state(DepGrStates.waiting_gr_teacher)

@router.message(DepGrStates.waiting_gr_teacher)
async def funG15(message: Message, state: FSMContext):
    dep_to_search = data_dep_dep.get(message.chat.id)
    group_to_search = message.text
    cursor.execute('SELECT name FROM teachers WHERE department LIKE ? AND groups LIKE ?', (f'%{dep_to_search}%', f'%{group_to_search}%', ))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'На этой кафедре пусто')
    await state.clear()
    await message.answer(f'Нашелся преподаватель: {st}')
    if len(results) >= 2:
        await message.answer(f'Введите ФИО преподавателя')
        await state.set_state(TeacherName1States.waiting_for_name1)
    else:
        await message.answer(f'Выберите действие', reply_markup = get_kb_contacts())

@router.message(TeacherName1States.waiting_for_name1)
async def fun_name(message: Message, state: FSMContext):
    name_to_search = message.text
    data_name_to_search[message.chat.id] = message.text
    await state.clear()
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ?',
                   (f'%{name_to_search}%',))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            st += "\n" + cleaned_row1 + ";" + cleaned_row2
    else:
        await message.answer(f'Ошибка')
    await state.clear()
    await message.answer(f'Нашелся преподаватель: {st}', reply_markup = get_kb_contacts())




@router.message(F.text == "Ввести ФИО преподавателя из списка💜")
async def fun17(message: Message, state: FSMContext):
    await message.answer(f'Введите ФИО преподавателя')
    await state.set_state(DepNameStates.waiting_name_teacher)




@router.message(DepNameStates.waiting_name_teacher)
async def funG17(message: Message, state: FSMContext):
    data_name_to_search[message.chat.id] = message.text
    dep_to_search = data_dep_dep.get(message.chat.id)
    name_to_search = message.text
    cursor.execute('SELECT name FROM teachers WHERE department LIKE ? AND name LIKE ?', (f'%{dep_to_search}%', f'%{name_to_search}%', ))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'В этой группе пусто')
    await state.clear()
    await message.answer(f'Нашелся преподаватель: {st}', reply_markup = get_kb_contacts())

@router.message(F.text == "Сделать фильтрацию по предмету💜")
async def fun16(message: Message, state: FSMContext):
    await message.answer(f'Введите название предмета')
    await state.set_state(TeacherSubSubStates.waiting_for_sub_sub)

@router.message(TeacherSubSubStates.waiting_for_sub_sub)
async def funG16(message: Message, state: FSMContext):
    dep_to_search = data_dep_dep.get(message.chat.id)
    sub_to_search = message.text
    cursor.execute('SELECT name FROM teachers WHERE department LIKE ? AND subjects LIKE ?',
                   (f'%{dep_to_search}%', f'%{sub_to_search}%',))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'На этой кафедре пусто')
    await state.clear()
    await message.answer(f'Нашелся преподаватель: {st}')
    if len(results) >= 2:
        await message.answer(f'Введите ФИО преподавателя')
        await state.set_state(TeacherName1States.waiting_for_name1)
    else:
        await message.answer(f'Выберите действие', reply_markup=get_kb_contacts())





@router.message(F.text == "Поиск по предмету")
async def reviews_bot(message: Message, state: FSMContext):
    await message.answer("Введите предмет, который ведет преподаватель")
    await state.set_state(SubStates.waiting_for_sub)

@router.message(SubStates.waiting_for_sub)
async def fun6(message: Message, state: FSMContext):
    data_sub[message.chat.id] = message.text
    await message.answer(f'Вы имеете в виду данный предмет - {data_sub.get(message.chat.id)}?', reply_markup=get_yes_no_sub())
    await state.clear()

@router.message(F.text == "Да, это верный предмет")
async def true_sub(message: Message):
    sub_to_search = data_sub.get(message.chat.id)
    cursor.execute('SELECT name FROM teachers WHERE subjects LIKE ?', (f'%{sub_to_search}%',))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'Никто не ведет данный предмет')
    await message.answer(f'Нашелся преподаватель: {st}', reply_markup = get_filtr_subject())

@router.message(F.text == "Нет, это неверный предмет")
async def false_sub(message: Message, state: FSMContext):
    await message.answer("Введите предмет, который ведет преподаватель")
    await state.set_state(SubStates.waiting_for_sub)

@router.message(F.text == "Ввести ФИО преподавателя из списка")
async def vvod_name(message: Message, state: FSMContext):
    await message.answer("Введите имя преподавателя")
    await state.set_state(NameStates.waiting_for_name)

@router.message(NameStates.waiting_for_name)
async def fun7(message: Message, state: FSMContext):
    sub_to_search = data_sub.get(message.chat.id)
    name_to_search = message.text
    cursor.execute('SELECT name, department FROM teachers WHERE name LIKE ? AND subjects LIKE ?', (f'%{name_to_search}%', f'%{sub_to_search}%'))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            st += "\n" + cleaned_row1 + "; " + cleaned_row2
    else:
        await message.answer(f'Никого не найдено')
    await message.answer(f'Нашелся преподаватель: {st}', reply_markup = get_kb_contacts())
    await state.clear()

@router.message(F.text == "Сделать фильтрацию по группе")
async def fil_group(message: Message, state: FSMContext):
    await message.answer("Введите вашу группу")
    await state.set_state(SubGrStates.waiting_for_g)

@router.message(SubGrStates.waiting_for_g)
async def fun9(message: Message, state: FSMContext):
    data_group_user[message.chat.id] = message.text
    sub_to_search = data_sub.get(message.chat.id)
    group_to_search = data_group_user.get(message.chat.id)
    cursor.execute('SELECT name, department FROM teachers WHERE groups LIKE ? AND subjects LIKE ?',(f'%{group_to_search}%', f'%{sub_to_search}%'))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            st += "\n" + cleaned_row1 + "; " + cleaned_row2
    else:
        await message.answer(f'Никого не найдено')
    await message.answer(f'Нашелся преподаватель: {st}')
    await state.clear()
    if len(results) >= 2:
        await message.answer(f'Введите ФИО преподавателя')
        await state.set_state(TeacherName1States.waiting_for_name1)
    else:
        data_name_to_search[message.chat.id] = cleaned_row1
        await message.answer(f'Выберите действие', reply_markup=get_kb_contacts())

@router.message(F.text == "Сделать фильтрацию по кафедре")
async def fil_dep(message: Message, state: FSMContext):
    await message.answer("Введите кафедру преподавателя")
    await state.set_state(SubDepStates.waiting_for_d)

@router.message(SubDepStates.waiting_for_d)
async def fun10(message: Message, state: FSMContext):
    data_dep_user[message.chat.id] = message.text
    sub_to_search = data_sub.get(message.chat.id)
    dep_to_search = f'Кафедра {data_dep_user.get(message.chat.id)}'
    #print(dep_to_search, sub_to_search )
    cursor.execute('SELECT name, department FROM teachers WHERE department LIKE ? AND subjects LIKE ?',(f'%{dep_to_search}%', f'%{sub_to_search}%'))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            st += "\n" + cleaned_row1 + "; " + cleaned_row2
    else:
        await message.answer(f'Никого не найдено')
    await message.answer(f'Нашелся преподаватель: {st}')
    await state.clear()

@router.message(F.text == "Поиск по группе")
async def search_gr(message: Message, state: FSMContext):
    await message.answer("Введите группу")
    await state.set_state(TeacherGroupStates.waiting_for_group_teacher)

@router.message(TeacherGroupStates.waiting_for_group_teacher)
async def funG(message: Message, state: FSMContext):
    await message.answer(f'Группа для поиска - {message.text}.')
    await state.clear()
    data_group_teacher[message.chat.id] = message.text
    group_to_search = message.text
    cursor.execute('SELECT name FROM teachers WHERE groups LIKE ?', (f'%{group_to_search}%',))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'В этой группе пусто')
    await message.answer(f'Нашелся преподаватель: {st}', reply_markup = get_fil_a())

@router.message(F.text == "Сделать фильтрацию по кафедре❤️")
async def fun11(message: Message, state: FSMContext):
    await message.answer(f'Введите номер кафедры')
    await state.set_state(TeacherGStates.waiting_for_g_teacher)

@router.message(TeacherGStates.waiting_for_g_teacher)
async def funG11(message: Message, state: FSMContext):
    group_to_search = data_group_teacher.get(message.chat.id)
    data_dep_u[message.chat.id] = message.text
    dep_to_search = data_dep_u.get(message.chat.id)
    cursor.execute('SELECT name FROM teachers WHERE groups LIKE ? AND department LIKE ?', (f'%{group_to_search}%', f'%{dep_to_search}%', ))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'В этой группе пусто')
    await state.clear()
    await message.answer(f'Нашелся преподаватель: {st}')
    if len(results) >= 2:
        await message.answer(f'Введите ФИО преподавателя')
        await state.set_state(TeacherName1States.waiting_for_name1)
    else:
        await message.answer(f'Выберите действие', reply_markup = get_kb_contacts())




@router.message(F.text == "Сделать фильтрацию по предмету❤️")
async def fun12(message: Message, state: FSMContext):
    await message.answer(f'Введите название предмета')
    await state.set_state(GrSubStates.waiting_for_sub_teacher)

@router.message(GrSubStates.waiting_for_sub_teacher)
async def funG12(message: Message, state: FSMContext):
    group_to_search = data_group_teacher.get(message.chat.id)
    data_sub_u[message.chat.id] = message.text
    sub_to_search = data_sub_u.get(message.chat.id)
    cursor.execute('SELECT name FROM teachers WHERE groups LIKE ? AND subjects LIKE ?', (f'%{group_to_search}%', f'%{sub_to_search}%', ))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'В этой группе пусто')
    await state.clear()
    await message.answer(f'Нашелся преподаватель: {st}')
    if len(results) >= 2:
        await message.answer(f'Введите ФИО преподавателя')
        await state.set_state(TeacherName1States.waiting_for_name1)
    else:
        await message.answer(f'Выберите действие', reply_markup = get_kb_contacts())





@router.message(F.text == "Ввести ФИО преподавателя из списка❤️")
async def fun13(message: Message, state: FSMContext):
    await message.answer(f'Введите ФИО преподавателя')
    await state.set_state(TeacherGrStates.waiting_name_teacher)





@router.message(TeacherGrStates.waiting_name_teacher)
async def funG13(message: Message, state: FSMContext):
    data_name_to_search[message.chat.id] = message.text
    group_to_search = data_group_teacher.get(message.chat.id)
    name_to_search = message.text
    cursor.execute('SELECT name FROM teachers WHERE groups LIKE ? AND name LIKE ?', (f'%{group_to_search}%', f'%{name_to_search}%', ))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            st += "\n" + cleaned_row1
    else:
        await message.answer(f'В этой группе пусто')
    await state.clear()
    await message.answer(f'Нашелся преподаватель: {st}', reply_markup = get_kb_contacts())

@router.message(F.text == "Контакты")
async def contacts(message: Message):
    name_to_search = data_name_to_search.get(message.chat.id)
    cursor.execute('SELECT name, contacts FROM teachers WHERE name LIKE ?',
                   (f'%{name_to_search}%',))
    results = cursor.fetchall()
    st = ""
    if results != []:
        for row in results:
            cleaned_row1 = row[0].strip()
            cleaned_row2 = row[1].strip()
            st += "\n" + cleaned_row1 + ". Контакты: " + cleaned_row2
    else:
        await message.answer(f'Ошибка')
    await message.answer(f'Нашелся преподаватель: {st}')

