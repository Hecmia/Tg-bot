from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Я студент", width = 2)
    kb.row(
        KeyboardButton(text ="Я преподаватель"),
        KeyboardButton(text="Книга отзывов тг бот"),
        KeyboardButton(text="Отзывы о преподавателях")
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)