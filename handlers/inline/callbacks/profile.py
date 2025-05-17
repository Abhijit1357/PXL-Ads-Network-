from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import register_publisher, get_profile_data, is_registered_user
from handlers.inline.keyboards import get_register_keyboard, get_back_keyboard

router = Router()

async def show_profile_with_back(callback: CallbackQuery, user_id: int, success_msg: str = ""):
    try:
        profile = await get_profile_data(user_id)
        if not profile:
            raise ValueError("Profile not found")
        text = (
            f"{success_msg}\n\n" if success_msg else "" +
            f"👤 <b>Your Profile</b>\n" +
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n" +
            f"💸 <b>Earnings:</b> ₹{profile['earnings']}\n" +
            f"👍 <b>Clicks:</b> {profile['clicks']}\n" +
            f"✅ <b>Approved:</b> {'Yes' if profile['approved'] else 'No'}"
        )
        await callback.message.edit_text(
            text,
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
    except Exception as e:
        print(f"Profile Display Error: {e}")
        await callback.message.edit_text(
            "⚠️ <b>Failed to load profile.</b>\nPlease try again.",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("⚠️ Error occurred.", show_alert=True)

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not await is_registered_user(user_id):
        await callback.message.edit_text(
            "⚠️ <b>Register First</b>\nClick Register to continue",
            reply_markup=get_register_keyboard(user_id=callback.from_user.id),
            parse_mode="HTML"
        )
        await callback.answer()
    else:
        await show_profile_with_back(callback, user_id)
        await callback.answer()
