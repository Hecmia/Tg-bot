from aiogram import Router, F, Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from config_reader import config
from aiogram.fsm.storage.memory import MemoryStorage
from models.create_reviews import ReviewsTeachers
from models.SessionLocal import SessionLocal, Session
from models.find import get_professor, get_subject


from keyboards.for_5 import get_kb_5
from keyboards.for_questions import get_kb
from keyboards.for_reviews import get_kb_reviews
from keyboards.for_do_you_know_teachers import get_kb_do_you_know_teacher
from keyboards.for_contacts import get_kb_contacts
from keyboards.for_schedule import get_kb_schedule
from keyboards.for_filters import get_kb_poisk
from keyboards.for_grops import get_kb_group
from keyboards.for_yes_no import get_yes_no_sub
from keyboards.for_fil2 import get_filtr_subject
from keyboards.for_fil3 import get_fil_a
from keyboards.for_fil4 import get_fil_c
from keyboards.for_fil5 import get_fil_b
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
import sqlite3

from config_reader import config

from aiogram.fsm.state import StatesGroup, State

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

class UserReviews(StatesGroup):
    teacher_name = State()
    strictness = State()
    scope_of_work = State()
    difficulty_of_delivery = State()
    attitude_to_attending_classes = State()
    keeps_his_word = State()
    mercy = State()
    the_subject = State()


bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=MemoryStorage())


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
    await message.answer("Введите номер вашей кафедры", reply_markup=ReplyKeyboardRemove())
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
    await message.answer("Введите номер вашей группы", reply_markup=ReplyKeyboardRemove())
    await state.set_state(StudentStates.waiting_for_group)

@router.message(StudentStates.waiting_for_group)
async def fun1(message: Message, state: FSMContext):
    data_users_student[message.chat.id] = message.text
    await message.answer(f'Отлично, ваша группа - {data_users_student.get(message.chat.id)}.')
    await state.clear()
    await message.answer(f'Вы знаете преподавателя?', reply_markup = get_kb_do_you_know_teacher())

@router.message(F.text == "Книга отзывов тг бот")
async def reviews_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы находитесь в блоке отзывов о тг боте")

@router.message(F.text == "Отзывы о преподавателях")
async def reviews_professors(message: Message):
    await message.answer("Вы находитесь в блоке отзывов о преподавателях", reply_markup=get_kb_reviews())


@router.message(F.text == "Добавить новый отзыв")
async def create_professor(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(UserReviews.teacher_name)
    await message.answer("Введите ФИО преподавателя", reply_markup=ReplyKeyboardRemove())

@router.message(UserReviews.teacher_name)
async def user_reviews_zero(message: Message, state: FSMContext):
    teacher_name = message.text.strip()
    teacher_dict = get_professor(teacher_name)
    id_teacher = teacher_dict["id"]
    professors_found = teacher_dict["name"]

    if professors_found:
        found_teacher_name = professors_found[0].strip()
        await state.update_data(teacher_name=found_teacher_name)
        await state.update_data(id_teacher=id_teacher[0])
        await state.set_state(UserReviews.the_subject)
        await message.answer("Введите предмет, который у вас вел преподаватель")

    else:
        await message.answer("Преподаватель с таким ФИО не найден. Попробуйте ввести снова.")
        await state.set_state(UserReviews.teacher_name)

@router.message(UserReviews.the_subject)
async def user_reviews_first(message: Message, state: FSMContext):
    the_subject = message.text.strip()
    subject_found = get_subject(the_subject)

    if subject_found:
        found_subject = subject_found
        await state.update_data(the_subject=found_subject)
        await state.set_state(UserReviews.strictness)
        await message.answer("Оцените СТРОГОСТЬ преподавателя по 5-ти бальной шкале", reply_markup=get_kb_5())

    else:
        await message.answer("Такой предмет не найден. Попробуйте ввести снова.")
        await state.set_state(UserReviews.the_subject)

@router.message(UserReviews.strictness)
async def user_reviews_second(message: Message, state: FSMContext):
    await state.update_data(strictness=message.text)
    await state.set_state(UserReviews.scope_of_work)
    await message.answer("Оцените ОБЪЕМ РАБОТ от преподавателя по 5-ти бальной шкале", reply_markup=get_kb_5())

@router.message(UserReviews.scope_of_work)
async def user_reviews_3(message: Message, state: FSMContext):
    await state.update_data(scope_of_work=message.text)
    await state.set_state(UserReviews.difficulty_of_delivery)
    await message.answer("Оцените СЛОЖНОСТЬ СДАЧИ РАБОТ преподавателю по 5-ти бальной шкале", reply_markup=get_kb_5())

@router.message(UserReviews.difficulty_of_delivery)
async def user_reviews_4(message: Message, state: FSMContext):
    await state.update_data(difficulty_of_delivery=message.text)
    await state.set_state(UserReviews.attitude_to_attending_classes)
    await message.answer("Оцените ОТНОШЕНИЕ ПРЕПОДАВАТЕЛЯ К ПОСЕЩЕНИЮ ПАР по 5-ти бальной шкале", reply_markup=get_kb_5())

@router.message(UserReviews.attitude_to_attending_classes)
async def user_reviews_5(message: Message, state: FSMContext):
    await state.update_data(attitude_to_attending_classes=message.text)
    await state.set_state(UserReviews.keeps_his_word)
    await message.answer("Оцените СДЕРЖИВАНИЕ СЛОВ преподавателя по 5-ти бальной шкале", reply_markup=get_kb_5())

@router.message(UserReviews.keeps_his_word)
async def user_reviews_6(message: Message, state: FSMContext):
    await state.update_data(keeps_his_word=message.text)
    await state.set_state(UserReviews.mercy)
    await message.answer("Оцените МИЛОСЕРДИЕ преподавателя по 5-ти бальной шкале", reply_markup=get_kb_5())

@router.message(UserReviews.mercy)
async def user_reviews_7(message: Message, state: FSMContext):
    await state.update_data(mercy=message.text)
    data = await state.get_data()

    session = Session()

    # Создайте новый отзыв и сохраните его в базе данных
    new_review = ReviewsTeachers(
        teacher_id=data["id_teacher"],
        the_subject=data["the_subject"],
        strictness=data["strictness"],
        scope_of_work=data["scope_of_work"],
        difficulty_of_delivery=data["difficulty_of_delivery"],
        attitude_to_attending_classes=data["attitude_to_attending_classes"],
        keeps_his_word=data["keeps_his_word"],
        mercy=data["mercy"],
    )

    session.add(new_review)
    session.commit()

    # Отправьте сообщение администратору с кнопками
    admin_chat_id = '704994121'
    await bot.send_message(admin_chat_id,
                           f"Новый отзыв от пользователя:\n\n{data}\n\n"
                           f"Одобрить? /approve_review_{new_review.id} /reject_review_{new_review.id}"
                           )

    await message.answer(
        f'Спасибо за ваш отзыв! Мы опубликуем его, если он пройдет модерацию!\n\nВаш отзыв:\n'
        f'ФИО преподавателя: {data["teacher_name"]}\n'
        f'Предмет, который вел у вас преподаватель: {data["the_subject"]}\n'
        f'Строгость преподавателя: {data["strictness"]}\n'
        f'Объем работ от преподавателя: {data["scope_of_work"]}\n'
        f'Сложность сдачи работ: {data["difficulty_of_delivery"]}\n'
        f'Отношение преподавателя к посещению пар: {data["attitude_to_attending_classes"]}\n'
        f'Достоверность слов преподавателя: {data["keeps_his_word"]}\n'
        f'Милосердие преподавателя: {data["mercy"]}',
        reply_markup=get_kb_reviews()
    )

    await state.clear()
    session.close()

@router.message(F.text.startswith('/approve_review_'))
async def approve_review(message: Message):
    review_id = int(message.text.split('_')[2])
    session = SessionLocal()
    try:
        session.expire_all()
        review = session.query(ReviewsTeachers).filter(ReviewsTeachers.id == review_id).first()
        if review:
            review.is_approved = True
            session.commit()
            await message.answer("Отзыв одобрен и будет опубликован.")
        else:
            await message.answer("Отзыв не найден.")
    except Exception as e:
        await message.answer("Произошла ошибка при одобрении отзыва.")
        print(f"Ошибка при одобрении отзыва: {e}")
    finally:
        session.close()

@router.message(F.text.startswith('/reject_review_'))
async def reject_review(message: Message):
    review_id = int(message.text.split('_')[2])
    session = SessionLocal()
    try:
        review = session.query(ReviewsTeachers).filter(ReviewsTeachers.id == review_id).first()
        if review:
            session.delete(review)
            session.commit()
            await message.answer("Отзыв отклонен и удален.")
        else:
            await message.answer("Отзыв не найден.")
    except Exception as e:
        await message.answer("Произошла ошибка при отклонении отзыва.")
        print(f"Ошибка при отклонении отзыва: {e}")
    finally:
        session.close()  # Закрываем сессию


@router.message(F.text == "Посмотреть отзывы")
async def view(message: Message):
    await message.answer("Введите ФИО преподавателя")

@router.message(F.text == "Назад")
async def go_back(message: Message, state: FSMContext):
    await message.answer("Вы находитесь на главном экране. Используйте меню для навигации.", reply_markup=get_kb())


@router.message(F.text == "Я знаю преподавателя")
async def i_know_teacher(message: Message, state: FSMContext):
    await message.answer("Введите ФИО преподавателя", reply_markup=ReplyKeyboardRemove())
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
    await message.answer("Введите ФИО преподавателя", reply_markup=ReplyKeyboardRemove())
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




