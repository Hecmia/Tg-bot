from aiogram import F, Router
from aiogram.types import CallbackQuery

from handlers.start import Message, FSMContext
from handlers.view_a_reviews import send_review
from keyboards.for_questions import get_kb
from keyboards.for_reviews import get_kb_reviews

router = Router()

@router.callback_query(F.data == "right")
async def on_right(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    reviews = data.get('reviews')
    current_review_index = data.get('current_review_index', 0)

    if current_review_index < len(reviews) - 1:
        current_review_index += 1
        await state.update_data(current_review_index=current_review_index)

        await send_review(callback_query.message, reviews, current_review_index, data.get('teacher_name'))

    await callback_query.answer()


@router.callback_query(F.data == "left")
async def on_left(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    reviews = data.get('reviews')
    current_review_index = data.get('current_review_index', 0)

    if current_review_index > 0:
        current_review_index -= 1
        await state.update_data(current_review_index=current_review_index)

        await send_review(callback_query.message, reviews, current_review_index, data.get('teacher_name'))

    await callback_query.answer()


@router.callback_query(F.data == "back")
async def on_back(callback_query: CallbackQuery, state: FSMContext):
    await state.clear()

    await callback_query.message.answer(
        "Вы вернулись в меню отзывов.",
        reply_markup=get_kb_reviews()
    )

    await callback_query.answer()


@router.message(F.text == "Назад")
async def go_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Вы находитесь на главном экране. Используйте меню для навигации.",
        reply_markup=get_kb()
    )