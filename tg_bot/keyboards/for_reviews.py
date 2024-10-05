from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_reviews()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Добавить новый отзыв")
    kb.button(text="Посмотреть отзывы")
    kb.button(text="Назад")
    kb.adjust(3)
    return kb.as_markup(resize_keyboard=True)
