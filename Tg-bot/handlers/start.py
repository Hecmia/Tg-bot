from aiogram import F, Bot, Dispatcher, Router
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from config_reader import config
from keyboards.for_questions import get_kb
from keyboards.for_reviews_bot import get_kb_reviews_bot
from handlers.class_state import UserReviews

from keyboards.for_do_you_know_teachers import get_kb_do_you_know_teacher

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=MemoryStorage())

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Приветствую вас! Это бот создан для удобного нахождения контактов и расписания преподавателей, а также отзывов о них. Выберите интересующий вас раздел!",
        reply_markup=get_kb()
    )


@router.message(F.text == "Книга отзывов тг бот")
async def reviews_bot(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Вы находитесь в блоке отзывов о тг боте", reply_markup = get_kb_reviews_bot())


@router.message(F.text == "Добавить новый отзыв о боте")
async def create_tg_bot(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(UserReviews.reviews_bot)
    await message.answer("Напишите свой отзыв", reply_markup=ReplyKeyboardRemove())


@router.message(F.text == "Поиск преподавателя")
async def search_teacher(message: Message):
    await message.answer(f"Вы знаете преподавателя?", reply_markup = get_kb_do_you_know_teacher())