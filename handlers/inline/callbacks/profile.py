from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db.models import get_profile_data, create_profile_if_not_exists
import handlers.inline.keyboards as keyboards

router = Router()

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    await create_profile_if_not_exists(user_id, username)
    profile = await get_profile_data(user_id)
    if profile:
        text = (
            f"👤 <b>Your Profile</b>\n"
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
            f"💸 <b>Earnings:</b> {profile.get('earnings', 0)}\n"
            f"👍 <b>Clicks:</b> {profile.get('clicks', 0)}"
        )
        await callback.message.edit_text(
            text,
            reply_markup=keyboards.get_back_keyboard(),
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            "⚠️ <b>Profile data not found.</b>\nPlease register first.",
            reply_markup=keyboards.get_back_keyboard(),
            parse_mode="HTML"
        )
    await callback.answer()
