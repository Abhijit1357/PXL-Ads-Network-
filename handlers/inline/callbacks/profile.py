from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import get_profile_data
import handlers.inline.keyboards as keyboards

router = Router()

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or ""
    
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
        text = (
            "⚠️ <b>Profile not found.</b>\n"
            "You need to register first to access your profile."
        )
        reply_markup = keyboards.get_register_keyboard()

    await callback.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    await callback.answer()
