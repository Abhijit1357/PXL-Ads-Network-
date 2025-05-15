from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import create_profile_if_not_exists
from utils.logger import log_to_group
import handlers.inline.keyboards as keyboards

router = Router()

@router.callback_query(lambda c: c.data == "register")
async def register_callback(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or "NoUsername"

    await create_profile_if_not_exists(user_id, username)

    log_msg = (
        f"✅ New user registered!\n\n"
        f"🆔 <code>{user_id}</code>\n"
        f"👤 Username: @{username}" if username != "NoUsername" else f"👤 Name: {callback.from_user.full_name}"
    )
    await log_to_group(callback.bot, log_msg)

    await callback.message.edit_text(
        "✅ <b>Registration successful!</b>\nClick '👤 Profile' again to view your profile.",
        parse_mode="HTML"
    )
    await callback.answer()
