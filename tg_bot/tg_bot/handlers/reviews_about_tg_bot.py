from aiogram import Router

from handlers.start import Message, FSMContext, ReplyKeyboardRemove
from class_state import UserReviews
from keyboards.for_reviews_bot import get_kb_reviews_bot
from models.SessionLocal import Session, SessionLocal
from models.create_reviews import ReviewsBot

router = Router()

@router.message(UserReviews.reviews_bot)
async def save_review(message: Message, state: FSMContext):
    user_id = message.from_user.id
    review_text = message.text.strip()

    db: Session = SessionLocal()

    try:
        new_review = ReviewsBot(creater=user_id, review=review_text)
        db.add(new_review)
        db.commit()
        await message.answer("Ваш отзыв был успешно добавлен!", reply_markup = get_kb_reviews_bot())
    except Exception as e:
        await message.answer("Произошла ошибка при добавлении отзыва. Попробуйте ввести отзыв заново.",
                             reply_markup=ReplyKeyboardRemove())

        await state.set_state(UserReviews.teacher_name)
    finally:
        db.close()

    await state.clear()