from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_kb_reviews() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить новый отзыв", width=2)
    kb.row(
        KeyboardButton(text="Посмотреть отзывы"),
        KeyboardButton(text="Назад")

    )
    kb.adjust(1)
    return kb.as_markup(resize_keyboard=True)