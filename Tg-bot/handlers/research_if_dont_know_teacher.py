from handlers.start import Message, ReplyKeyboardRemove
from keyboards.for_filters import get_kb_poisk
from aiogram import Router, F


router = Router()


@router.message(F.text == "Я не знаю преподавателя")
async def i_know_teacher(message: Message):
    await message.answer("Выберите фильтр для поиска", reply_markup=get_kb_poisk())


