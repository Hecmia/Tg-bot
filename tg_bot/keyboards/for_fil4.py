from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_fil_c() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Сделать фильтрацию по предмету", width=2)
    kb.row(

        KeyboardButton(text="Введсти ФИО преподавателя из списка")

    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)