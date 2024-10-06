from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_schedule()->ReplyKeyboardMarkup:
  kb = ReplyKeyboardBuilder()
  kb.button(text="Выбрать день", width=2)
  kb.row(
    KeyboardButton(text="Показать данную неделю"),
    KeyboardButton(text="Показать следующую неделю")
  )
  kb.adjust(1)
  return kb.as_markup(resize_keyboard=True)