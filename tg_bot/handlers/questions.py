from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.for_questions import get_kb
from keyboards.for_reviews import get_kb_reviews

router = Router()

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
async def reviews_bot(message: Message):
    await message.answer("Вы находитесь в блоке отзывов о тг боте")

@router.message(F.text == "Отзывы о преподавателях")
async def reviews_professors(message: Message):
    await message.answer("Вы находитесь в блоке отзывов о преподавателях", reply_markup=get_kb_reviews())

@router.message(F.text == "Добавить новый отзыв")
async def create_professor(message: Message):
    await message.answer("Введите ФИО преподавателя")

@router.message(F.text == "Посмотреть отзывы")
async def view(message: Message):
    await message.answer("Введите ФИО преподавателя")