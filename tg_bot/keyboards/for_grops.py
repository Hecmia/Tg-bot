from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_kb_group()->ReplyKeyboardMarkup:
  kb = ReplyKeyboardBuilder()
  kb.button(text="Указать другую группу", width=2)
  kb.row(
    KeyboardButton(text="Поиск по своей группе")
  )
  kb.adjust(1)
  return kb.as_markup(resize_keyboard=True)