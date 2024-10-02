from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_do_you_know_teacher()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Я знаю преподавателя")
    kb.button(text="Я не знаю преподавателя")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)