from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import get_profile_data, create_profile_if_not_exists
import handlers.inline.keyboards as keyboards

router = Router()

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or ""

    # Ensure profile exists or create if new user
    await create_profile_if_not_exists(user_id, username)

    # Get updated profile
    profile = await get_profile_data(user_id)

    # If profile not found, provide default data
    if not profile:
        profile = {
            "earnings": 0,
            "clicks": 0,
            "approved": False,
            "bot_link": ""
        }

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
