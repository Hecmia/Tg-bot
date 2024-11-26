from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_contacts()->ReplyKeyboardMarkup:
  kb = ReplyKeyboardBuilder()
  kb.button(text="Информация о преподавателе", width=2)
  kb.row(
    KeyboardButton(text="Не тот преподаватель"),
    KeyboardButton(text="Главное меню")
  )
  kb.adjust(1)
  return kb.as_markup(resize_keyboard=True)
