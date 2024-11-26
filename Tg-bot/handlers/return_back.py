from handlers.start import Message, FSMContext, ReplyKeyboardRemove, CallbackQuery
from aiogram import Router, F
from keyboards.for_questions import get_kb


router = Router()


@router.message(F.text == "Главное меню")
async def main_menu(message: Message):
    await message.answer("Вы находитесь на главном экране. Используйте меню для навигации.", reply_markup=get_kb())


@router.callback_query(F.data == "back1")
async def go_home(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Вы находитесь на главном экране. Используйте меню для навигации.", reply_markup=get_kb())
