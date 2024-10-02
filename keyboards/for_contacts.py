from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_contacts()->ReplyKeyboardMarkup:
  kb = ReplyKeyboardBuilder()
  kb.button(text="Контакты", width=2)
  kb.row(
    KeyboardButton(text="Расписание"),
    KeyboardButton(text="Не тот преподаватель")
  )
  kb.adjust(1)
  return kb.as_markup(resize_keyboard=True)