from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_kb_day():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ПН", callback_data = "Понедельник")],
        [InlineKeyboardButton(text ="ВТ", callback_data = "Вторник")],
        [InlineKeyboardButton(text="СР", callback_data = "Среда") ],
        [InlineKeyboardButton(text="ЧТ", callback_data = "Четверг")],
        [InlineKeyboardButton(text="ПТ", callback_data="Пятница")],
        [InlineKeyboardButton(text="СБ", callback_data="Суббота")]
    ])
    return kb