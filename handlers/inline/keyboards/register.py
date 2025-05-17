from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models import is_registered_user

async def get_register_keyboard(user_id: int):
    #"""Only shows register button if user isn't registered"""
    if await is_registered_user(user_id):
        return None  # Returns None if user is registered
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Accept & Register", callback_data="register_accept")]
    ])
