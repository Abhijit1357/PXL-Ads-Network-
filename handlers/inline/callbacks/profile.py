from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import get_profile_data, register_user, user_exists
import handlers.inline.keyboards as keyboards

router = Router()

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or ""

    # Register if user not exists
    if not await user_exists(user_id):
        await register_user(user_id, username)
        await callback.message.answer("✅ Registration successful!")

    # Get profile data again after registration
    profile = await get_profile_data(user_id)

    if profile:
        text = (
            f"👤 <b>Your Profile</b>\n"
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
            f"💸 <b>Earnings:</b> ₹{profile.get('earnings', 0)}\n"
            f"👍 <b>Clicks:</b> {profile.get('clicks', 0)}"
        )
        reply_markup = keyboards.get_back_keyboard()
    else:
        # Shouldn't happen but as a fallback
        text = (
            "⚠️ <b>Profile not found.</b>\n"
            "Please try again later."
        )
        reply_markup = keyboards.get_back_keyboard()

    await callback.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    await callback.answer()
