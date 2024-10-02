from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Я студент")
    kb.button(text="Я преподаватель")
    kb.button(text="Книга отзывов тг бот")
    kb.button(text="Отзывы о преподавателях")
    kb.adjust(4)
    return kb.as_markup(resize_keyboard=True)

