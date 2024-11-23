from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.start import Message, FSMContext, ReplyKeyboardRemove,bot
from class_state import UserReviews
from keyboards.for_5 import get_kb_5
from keyboards.for_reviews import get_kb_reviews
from models.SessionLocal import Session
from models.create_reviews import ReviewsTeachers
from models.find import get_professor, get_subject
from config_reader import Settings

router = Router()

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
        await ask_for_rating(message.chat.id, "Оцените СТРОГОСТЬ преподавателя по 5-ти бальной шкале, где 1 - нестрого, а 5 - очень строго", state, message_id=None)
    else:
        await message.answer("Такой предмет не найден. Попробуйте ввести снова.")
        await state.set_state(UserReviews.the_subject)


async def ask_for_rating(chat_id, question, state, message_id=None):
    await state.update_data(current_question=question)
    await state.update_data(current_question=question)
    kb = get_kb_5()

    if message_id:

        await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=question, reply_markup=kb)
    else:

        message = await bot.send_message(chat_id, question, reply_markup=kb)
        await state.update_data(message_id=message.message_id)


@router.callback_query(F.data.startswith("rating_"))
async def user_reviews_rating(call: CallbackQuery, state: FSMContext):
    rating = call.data.split("_")[1]
    data = await state.get_data()

    message_id = data.get("message_id")
    current_state = await state.get_state()

    if current_state == UserReviews.strictness.state:
        await state.update_data(strictness=rating)
        await state.set_state(UserReviews.scope_of_work)
        await ask_for_rating(call.message.chat.id,
                             "Оцените ОБЪЕМ РАБОТ от преподавателя по 5-ти бальной шкале, где 1 - мало, а 5 - очень много",
                             state, message_id)

    elif current_state == UserReviews.scope_of_work.state:
        await state.update_data(scope_of_work=rating)
        await state.set_state(UserReviews.difficulty_of_delivery)
        await ask_for_rating(call.message.chat.id,
                             "Оцените СЛОЖНОСТЬ СДАЧИ РАБОТ преподавателю по 5-ти бальной шкале, где 1 - несложно, а 5 - очень сложно",
                             state, message_id)

    elif current_state == UserReviews.difficulty_of_delivery.state:
        await state.update_data(difficulty_of_delivery=rating)
        await state.set_state(UserReviews.attitude_to_attending_classes)
        await ask_for_rating(call.message.chat.id,
                             "Оцените ОТНОШЕНИЕ ПРЕПОДАВАТЕЛЯ К ПОСЕЩЕНИЮ ПАР по 5-ти бальной шкале, где 1 - ему пофиг, а 5 - убьет за пропущенную пару",
                             state, message_id)

    elif current_state == UserReviews.attitude_to_attending_classes.state:
        await state.update_data(attitude_to_attending_classes=rating)
        await state.set_state(UserReviews.keeps_his_word)
        await ask_for_rating(call.message.chat.id,
                             "Оцените СДЕРЖИВАНИЕ СЛОВ преподавателя по 5-ти бальной шкале, где 1 - любит обманывать, а 5 - всегда держит обещания",
                             state, message_id)

    elif current_state == UserReviews.keeps_his_word.state:
        await state.update_data(keeps_his_word=rating)
        await state.set_state(UserReviews.mercy)
        await ask_for_rating(call.message.chat.id,
                             "Оцените МИЛОСЕРДИЕ преподавателя по 5-ти бальной шкале, где 1 - милосердия нет, а 5 - очень милосердный",
                             state, message_id)

    elif current_state == UserReviews.mercy.state:
        await state.update_data(mercy=rating)
        await state.set_state(UserReviews.note)
        await call.message.answer("Пожалуйста, оставьте ваше примечание к отзыву (если его нет, напишите слово Нет):")


@router.message(UserReviews.note)
async def user_reviews_note_handler(message: Message, state: FSMContext, default_admin=None):
    note = message.text.strip()
    config = Settings()
    default_admin = config.default_admin

    await state.update_data(note=note)
    data = await state.get_data()

    session = Session()
    new_review = ReviewsTeachers(
        teacher_id=data["id_teacher"],
        the_subject=data["the_subject"],
        strictness=data["strictness"],
        scope_of_work=data["scope_of_work"],
        difficulty_of_delivery=data["difficulty_of_delivery"],
        attitude_to_attending_classes=data["attitude_to_attending_classes"],
        keeps_his_word=data["keeps_his_word"],
        mercy=data["mercy"],
        note=note
    )

    session.add(new_review)
    session.commit()

    await bot.send_message(default_admin,
                           f"Новый отзыв от пользователя:\n\n{data}\nПримечание: {note}\n\n"
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
        f'Милосердие преподавателя: {data["mercy"]}\n'
        f'Примечание: {note if note else "Нет примечания."}',
        reply_markup=get_kb_reviews()
    )

    await state.clear()
    session.close()


