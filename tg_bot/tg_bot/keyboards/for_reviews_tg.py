from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_kb_reviews_tg():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="<", callback_data="left"),
            InlineKeyboardButton(text=">", callback_data="right"),
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back"),
            InlineKeyboardButton(text="Среднее значение", callback_data="average_reviews")
        ]
    ])
    return kb


def get_kb_reviews_inline() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="back")  # Обработчик через callback_data
        ]
    ])
    return kb
