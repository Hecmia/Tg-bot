from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.start import Message, FSMContext, ReplyKeyboardRemove
from handlers.class_state import UserReviews
from keyboards.for_reviews_tg import get_kb_reviews_tg, get_kb_reviews_inline
from models.find import get_reviews, get_average_reviews
from models.SessionLocal import SessionLocal

router = Router()

@router.message(F.text == "Посмотреть отзывы")
async def view(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите ФИО преподавателя", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserReviews.waiting_for_teacher_name)


@router.message(UserReviews.waiting_for_teacher_name)
async def get_teacher_name(message: Message, state: FSMContext):
    teacher_name = message.text.strip()
    await state.update_data(teacher_name=teacher_name)
    await message.answer("Введите интересующий вас предмет", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserReviews.waiting_for_subject)


@router.message(UserReviews.waiting_for_subject)
async def get_teacher_reviews(message: Message, state: FSMContext):
    subject = message.text.strip()
    data = await state.get_data()
    teacher_name = data.get('teacher_name')

    await state.update_data(subject=subject)

    reviews, teacher_name = get_reviews(teacher_name, subject)

    if reviews:
        await state.update_data(reviews=reviews, current_review_index=0)
        message_id = data.get('message_id')
        if not message_id:
            sent_message = await send_review(message, reviews, 0, teacher_name, is_new_message=True)
            await state.update_data(message_id=sent_message.message_id)
        else:
            await send_review(message, reviews, 0, teacher_name, is_new_message=False)
    else:
        await state.clear()
        await message.answer(f"Отзывы о преподавателе {teacher_name} не найдены.\nПопробуйте ввести ФИО снова.")
        await state.set_state(UserReviews.waiting_for_teacher_name)


async def send_review(message: Message, reviews, index, teacher_name, is_new_message=False):
    review = reviews[index]
    response = (
        f"Отзывы о преподавателе {teacher_name}:\n\n"
        f"Предмет: {review.the_subject}\n"
        f"Строгость: {review.strictness}\n"
        f"Объем работы: {review.scope_of_work}\n"
        f"Сложность сдачи: {review.difficulty_of_delivery}\n"
        f"Отношение к посещению: {review.attitude_to_attending_classes}\n"
        f"Достоверность слов: {review.keeps_his_word}\n"
        f"Милосердие: {review.mercy}\n"
        f"Примечание: {review.note}\n"
    )
    reply_markup = get_kb_reviews_tg() if len(reviews) > 1 else get_kb_reviews_inline()

    if is_new_message:
        sent_message = await message.answer(response, reply_markup=reply_markup)
        return sent_message
    else:
        try:
            await message.bot.edit_message_text(
                text=response,
                chat_id=message.chat.id,
                message_id=message.message_id,
                reply_markup=reply_markup
            )

        except Exception as e:
            print(f"Ошибка при редактировании сообщения: {e}")


def stars_rating(average):
    if average is None:
        return "Не доступно"
    return "⭐" * round(average)

@router.callback_query(F.data == "average_reviews")
async def average_review(callback_query: CallbackQuery, state: FSMContext):
    try:
        data = await state.get_data()
        teacher_name = data.get('teacher_name')
        subject = data.get('subject')

        if not teacher_name or not subject:
            await callback_query.message.answer("Произошла ошибка, попробуйте снова.")
            return
    except Exception:
        await callback_query.message.answer("Произошла ошибка при получении данных.")
        return

    try:
        session = SessionLocal()
        averages = get_average_reviews(teacher_name, subject, session)
        session.close()
    except Exception as e:
        await callback_query.message.answer(f"Произошла ошибка при запросе данных: {e}")
        return

    if averages:
        response = (
            f"Среднее значение по преподавателю {teacher_name} по предмету {subject}:\n\n"
            f"Строгость: {stars_rating(averages[0])}\n"
            f"Объем работы: {stars_rating(averages[1])}\n"
            f"Сложность сдачи: {stars_rating(averages[2])}\n"
            f"Отношение к посещению: {stars_rating(averages[3])}\n"
            f"Достоверность слов: {stars_rating(averages[4])}\n"
            f"Милосердие: {stars_rating(averages[5])}\n"
        )

        message_id = data.get('message_id')
        if not message_id:
            sent_message = await callback_query.message.answer(response, reply_markup=get_kb_reviews_inline())
            await state.update_data(message_id=sent_message.message_id)

        else:
            try:
                await callback_query.message.bot.edit_message_text(
                    text=response,
                    chat_id=callback_query.message.chat.id,
                    message_id=message_id,
                    reply_markup=get_kb_reviews_inline()
                )
            except Exception as e:
                print(f"Ошибка при редактировании сообщения: {e}")
                await callback_query.message.answer("Произошла ошибка при редактировании сообщения.")
    else:
        await callback_query.message.answer("Средние значения не найдены для этого преподавателя и предмета.")
