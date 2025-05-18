from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import register_publisher, get_profile_data, is_registered_user
from handlers.inline.keyboards import get_register_keyboard, get_back_keyboard

router = Router()

async def show_profile_with_back(callback: CallbackQuery, user_id: int, success_msg: str = ""):
    try:
        if not await is_registered_user(user_id):
            await callback.message.edit_text(
                "⚠️ <b>You are not registered.</b>\nClick Register to continue",
                reply_markup=await get_register_keyboard(user_id),
                parse_mode="HTML"
            )
            return
        
        profile = await get_profile_data(user_id)
        if not profile:
            profile = {
                "earnings": 0,
                "clicks": 0,
                "approved": False
            }
        
        text = (
            f"{success_msg}\n\n" if success_msg else "" +
            f"👤 <b>Your Profile</b>\n" +
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n" +
            f"💸 <b>Earnings:</b> ₹{profile.get('earnings', 0)}\n" +
            f"👍 <b>Clicks:</b> {profile.get('clicks', 0)}\n" +
            f"✅ <b>Approved:</b> {'Yes' if profile.get('approved', False) else 'No'}"
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
    await show_profile_with_back(callback, user_id)
    await callback.answer()
