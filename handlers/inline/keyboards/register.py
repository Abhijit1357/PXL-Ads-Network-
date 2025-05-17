from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models import is_registered_user

async def get_register_keyboard(user_id: int):
    #"""Returns None if user is registered"""
    is_registered = await is_registered_user(user_id)
    print(f"User {user_id} registered status: {is_registered}")  # Debugging
    if is_registered:
        return None  # Hide register button
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Accept & Register", callback_data="register_accept")]
    ])
