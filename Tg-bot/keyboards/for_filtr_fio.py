from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_filtr_fio()->ReplyKeyboardMarkup:
  kb = ReplyKeyboardBuilder()
  kb.button(text="Ввести ФИО преподавателя из списка", width=2)
  kb.row(
    KeyboardButton(text="Сделать фильтрацию по группе"),
    KeyboardButton(text="Сделать фильтрацию по кафедре"),
    KeyboardButton(text="Главное меню")

  )
  kb.adjust(1)
  return kb.as_markup(resize_keyboard=True)