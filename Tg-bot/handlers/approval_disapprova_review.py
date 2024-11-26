from aiogram import F, Router

from handlers.start import Message
from models.create_reviews import ReviewsTeachers
from models.SessionLocal import SessionLocal

router = Router()

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
        session.close()