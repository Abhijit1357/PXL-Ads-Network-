from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import create_profile_if_not_exists, get_profile
from utils.logger import log_to_group
from handlers.inline.keyboards import get_back_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "register_accept")
async def register_callback(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        username = callback.from_user.username or "NoUsername"

        # Create profile if not exists
        await create_profile_if_not_exists(user_id, username)

        # Fetch profile from DB
        profile = await get_profile(user_id)
        if not profile:
            raise ValueError("Profile not found after creation")

        # Log registration
        log_msg = (
            f"✅ New user registered!\n\n"
            f"🆔 <code>{user_id}</code>\n"
            f"👤 Username: @{username}" if username != "NoUsername" else
            f"👤 Name: {callback.from_user.full_name}"
        )
        await log_to_group(callback.bot, log_msg)

        # Show profile directly
        await callback.message.edit_text(
            f"✅ <b>Registration Successful!</b>\n\n"
            f"👤 <b>Your Profile</b>\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"💸 Earnings: ₹{profile['earnings']}\n"
            f"👍 Clicks: {profile['clicks']}",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("🎉 Registered!")

    except Exception as e:
        # Detailed logging
        error_msg = f"Registration Error for user {user_id}: {str(e)}"
        print(error_msg)
        await log_to_group(callback.bot, error_msg)  # Log to Telegram group for visibility

        # Show user-friendly error
        await callback.message.edit_text(
            "⚠️ <b>Registration failed.</b>\nPlease try again.",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("⚠️ Registration failed.", show_alert=True)
