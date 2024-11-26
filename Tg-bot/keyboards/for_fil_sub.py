from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_fil_sub() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Сделать фильтрацию по предмету", width=2)
    kb.row(

        KeyboardButton(text="Ввести ФИО преподавателя из списка"),
        KeyboardButton(text="Главное меню")
    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)