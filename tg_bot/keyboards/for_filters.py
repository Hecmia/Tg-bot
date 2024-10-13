from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_kb_poisk() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Поиск по группе", width=2)
    kb.row(
        KeyboardButton(text="Поиск по предмету"),
        KeyboardButton(text="Поиск по кафедре")

    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)