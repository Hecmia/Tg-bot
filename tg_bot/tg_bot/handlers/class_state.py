from aiogram.fsm.state import StatesGroup, State


class UserReviews(StatesGroup):
    teacher_name = State()
    strictness = State()
    scope_of_work = State()
    difficulty_of_delivery = State()
    attitude_to_attending_classes = State()
    keeps_his_word = State()
    mercy = State()
    the_subject = State()
    reviews_bot = State()
    note = State()
    waiting_for_teacher_name = State()
    waiting_for_subject = State()