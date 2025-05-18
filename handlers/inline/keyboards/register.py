from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_register_keyboard(user_id: int = None):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Accept & Register", callback_data="register_accept")]
    ])

reply_markup = get_register_keyboard(user_id=callback.from_user.id)
