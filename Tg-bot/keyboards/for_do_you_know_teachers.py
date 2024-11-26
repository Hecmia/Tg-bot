from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_do_you_know_teacher()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Я знаю преподавателя", width = 2)
    kb.row(

        KeyboardButton(text="Я не знаю преподавателя"),
        KeyboardButton(text="Главное меню")
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)