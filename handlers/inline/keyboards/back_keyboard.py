from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Back", callback_data="go_back")]
    ])
