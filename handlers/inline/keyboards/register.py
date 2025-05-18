from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_register_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Accept & Register", callback_data="register_accept")]
    ])
