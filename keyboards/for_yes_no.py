from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_yes_no_sub()->ReplyKeyboardMarkup:
  kb = ReplyKeyboardBuilder()
  kb.button(text="Да, это верный предмет", width=2)
  kb.row(
    KeyboardButton(text="Нет, это неверный предмет")

  )
  kb.adjust(1)
  return kb.as_markup(resize_keyboard=True)