from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_kb_5():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1", callback_data="rating_1"),
            InlineKeyboardButton(text="2", callback_data="rating_2"),
            InlineKeyboardButton(text="3", callback_data="rating_3"),
            InlineKeyboardButton(text="4", callback_data="rating_4"),
            InlineKeyboardButton(text="5", callback_data="rating_5")
        ],
        [
            InlineKeyboardButton(text="Назад", callback_data="back")
        ]
    ])
    return kb
