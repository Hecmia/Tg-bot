from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_5()->ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="1")
    kb.button(text="2")
    kb.button(text="3")
    kb.button(text="4")
    kb.button(text="5")
    kb.adjust(5)
    return kb.as_markup(resize_keyboard=True)