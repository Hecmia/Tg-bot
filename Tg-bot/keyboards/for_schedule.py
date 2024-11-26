from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
def get_kb_schedule():
  kb = InlineKeyboardMarkup(inline_keyboard=[
        [
          InlineKeyboardButton(text="Выбрать день", callback_data = "Выбрать день")
        ],
        [ InlineKeyboardButton(text="Показать полное расписание", callback_data = "Показать полное расписание")],
        [  InlineKeyboardButton(text="Показать четную неделю", callback_data = "Показать четную неделю") ],
        [  InlineKeyboardButton(text="Показать нечетную неделю", callback_data = "Показать нечетную неделю")],
        [ InlineKeyboardButton(text="Контакты", callback_data="Контакты")],
        [InlineKeyboardButton(text="Главное меню", callback_data="back1")]
        ])
  return kb
