import keyboards.for_5 as for_5
import keyboards.for_questions as for_questions
import keyboards.for_reviews as for_reviews
import keyboards.for_reviews_bot as for_reviews_bot
import keyboards.for_reviews_tg as for_reviews_tg
import config_reader as config_reader

from aiogram import Router
from .approval_disapprova_review import router as approval_disapprova_review
from .reviews_about_teachers import router as reviews_about_teachers
from .reviews_about_tg_bot import router as reviews_about_tg_bot
from .reviews_button_handler import router as reviews_button_handler
from .start import router as start_router
from .view_a_reviews import router as view_a_reviews

router = Router()

router.include_routers(
    approval_disapprova_review,
    reviews_about_teachers,
    reviews_about_tg_bot,
    reviews_button_handler,
    start_router,
    view_a_reviews
)