from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_register_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Register Now", callback_data="register")]
    ])
