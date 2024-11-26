from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
def kb_no_dep()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Ввести кафедру", width = 2)
    kb.row(
        KeyboardButton(text="Главное меню")
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)