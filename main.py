import logging
import asyncio
from aiogram.utils import markdown
from lib2to3.btm_utils import tokens
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButtonPollType,
)
from aiogram.filters import CommandStart, Command
from aiogram import F, Router, types
#from aiogram.filters import StatesGroup, State
from aiogram.fsm.state import State, StatesGroup
#from aiogram.dispatcher import FSMContext
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardBuilder
BOT_TOKEN = ""
router = Router(name=__name__)

users = {}

class UserState(StatesGroup):
    group = State()
    #teacher = State()

class ButtonText:
    teachers = "Я преподаватель"
    student = "Я студент"
    book_b= "Книга отзывов и предложений о тг-боте"
    book_t = "Отзывы о преподавателях"

bot = Bot(token = BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def answer(message: types.Message):
    info = 'Приветствую вас! Это бот создан для удобного нахождения контактов и расписания преподавателей, а также отзывов о них. Выберите интересующий вас раздел!'
    await message.answer( text = info, reply_markup=get_on_start_kb())

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

def get_on_start_kb() -> ReplyKeyboardMarkup:
    button_teachers = KeyboardButton(text=ButtonText.teachers)
    button_student = KeyboardButton(text=ButtonText.student)
    button_book_b = KeyboardButton(text=ButtonText.book_b)
    button_book_t = KeyboardButton(text=ButtonText.book_t)
    buttons_first_row = [button_teachers, button_student]
    buttons_second_row = [button_book_b]
    buttons_third_row = [button_book_t]
    markup = ReplyKeyboardMarkup(
        keyboard = [buttons_first_row, buttons_second_row, buttons_third_row],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
    return markup




#@router.message(F.text == ButtonText.student)
@dp.message(F.text =="Я студент")
async def answer_s(message: types.Message, state:FSMContext):

    chat_id = message.chat.id
    await message.answer(text="Введите номер вашей группы")
    users[chat_id] = {}
    #await message.answer(reply_markup = save_group)
    @dp.message()
    async def test_func():
        await handlers.save_group(text)
    #await handlers.save_group(text)
    #await UserState.group.set()


#@dp.message(F.state==UserState.group)
#async def save_group(message: types.Message, state: FSMContext):
async def save_group(message: types.Message):
    chat_id = message.chat.id
    group = message.text
    users[chat_id]['group'] = group
    await message.answer(f'Отлично, ваша группа - {group}.')
    await state.finish()
    await show_next_buttons(message)


'''@dp.message(F.text =="Я преподаватель")
async def answer_t(message: types.Message):
    await message.answer(
        text="Введите номер вашей кафедры",
        #reply_markup=ReplyKeyboardRemove(),
    )'''

'''@dp.message(F.text =="Я преподаватель")
async def answer_t(message: types.Message):
    await message.answer(
        text="Введите номер вашей кафедры",
        #reply_markup=ReplyKeyboardRemove(),
    )'''

if __name__ == "__main__":
    asyncio.run(main())
