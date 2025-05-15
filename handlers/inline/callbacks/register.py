# handlers/inline/callbacks/register.py
from aiogram import Router
from aiogram.types import CallbackQuery
import handlers.inline.keyboards as keyboards
from db.models import create_profile_if_not_exists, get_profile_data
from utils.logger import log_to_group

router = Router()

@router.callback_query(lambda c: c.data == "register_accept")
async def register_callback(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        username = callback.from_user.username or "NoUsername"

        # Create profile and get data
        await create_profile_if_not_exists(user_id, username)
        profile = await get_profile_data(user_id)

        # Logging
        log_msg = (f"✅ New user: {user_id}\n"
                  f"👤 {'@'+username if username!='NoUsername' else callback.from_user.full_name}")
        await log_to_group(callback.bot, log_msg)

        # Show success message with profile AND back button
        await callback.message.edit_text(
            f"✅ <b>Registration successful!</b>\n\n"
            f"👤 <b>Your Profile</b>\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"💸 Earnings: ₹{profile['earnings']}",
            reply_markup=keyboards.get_back_keyboard(),  # Added back button
            parse_mode="HTML"
        )
        await callback.answer()
        
    except Exception as e:
        print(f"Registration Error: {e}")
        await callback.answer("⚠️ Registration failed", show_alert=True)
