from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import get_profile_data, is_registered_user
import handlers.inline.keyboards as keyboards

router = Router()

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id

    # Check if user is registered
    is_registered = await is_registered_user(user_id)

    if not is_registered:
        text = (
            "⚠️ <b>You are not registered.</b>\n"
            "Please register first to view your profile."
        )
        reply_markup = keyboards.get_register_keyboard()
    else:
        profile = await get_profile_data(user_id)
        text = (
            f"👤 <b>Your Profile</b>\n"
            f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
            f"💸 <b>Earnings:</b> ₹{profile['earnings']}\n"
            f"👍 <b>Clicks:</b> {profile['clicks']}\n"
            f"✅ <b>Approved:</b> {'Yes' if profile['approved'] else 'No'}"
        )
        reply_markup = keyboards.get_back_keyboard()

    await callback.message.edit_text(
        text,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )
    await callback.answer()
