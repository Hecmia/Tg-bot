from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards.for_5 import get_kb_5
from keyboards.for_questions import get_kb
from keyboards.for_reviews import get_kb_reviews
from models.create_reviews import ReviewsTeachers
from models.SessionLocal import SessionLocal, Session
from models.find import get_professor, get_subject
from config_reader import config

router = Router()
bot = Bot(token=config.bot_token.get_secret_value())

class UserReviews(StatesGroup):
    teacher_name = State()
    strictness = State()
    scope_of_work = State()
    difficulty_of_delivery = State()
    attitude_to_attending_classes = State()
    keeps_his_word = State()
    mercy = State()
    the_subject = State()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Приветствую вас! Это бот создан для удобного нахождения контактов и расписания преподавателей, а также отзывов о них. Выберите интересующий вас раздел!",
        reply_markup=get_kb()
    )

@router.message(F.text == "Я преподаватель")
async def i_professor(message: Message):
    await message.answer("Введите номер вашей кафедры")

@router.message(F.text == "Я студент")
async def i_student(message: Message):
    await message.answer("Введите номер вашей группы")

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