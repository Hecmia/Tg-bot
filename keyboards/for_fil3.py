from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_fil_a()->ReplyKeyboardMarkup:
  kb = ReplyKeyboardBuilder()
  kb.button(text="Сделать фильтрацию по кафедре❤️", width=2)
  kb.row(
    KeyboardButton(text="Сделать фильтрацию по предмету❤️"),
    KeyboardButton(text="Ввести ФИО преподавателя из списка❤️")

  )
  kb.adjust(1)
  return kb.as_markup(resize_keyboard=True)