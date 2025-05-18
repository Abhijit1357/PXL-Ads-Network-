from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_register_keyboard(user_id: int):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="📝 Register", callback_data=f"register_{user_id}")
    )
    return keyboard
