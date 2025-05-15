from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import create_profile_if_not_exists
from utils.logger import log_to_group
from handlers.inline.keyboards import get_back_keyboard  # <-- Added import

router = Router()

@router.callback_query(lambda c: c.data == "register_accept")
async def register_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or "NoUsername"

    await create_profile_if_not_exists(user_id, username)

    # Proper logging message
    if username != "NoUsername":
        log_msg = (
            f"✅ New user registered!\n\n"
            f"🆔 <code>{user_id}</code>\n"
            f"👤 Username: @{username}"
        )
    else:
        log_msg = (
            f"✅ New user registered!\n\n"
            f"🆔 <code>{user_id}</code>\n"
            f"👤 Name: {callback.from_user.full_name}"
        )

    await log_to_group(callback.bot, log_msg)

    # Edited text with back button
    await callback.message.edit_text(
        "✅ <b>Registration successful!</b>\nClick '👤 Profile' again to view your profile.",
        reply_markup=get_back_keyboard(),
        parse_mode="HTML"
    )
    await callback.answer()
