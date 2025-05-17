from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from db.models import get_profile_data, is_registered_user
from handlers.inline.keyboards import get_register_keyboard, get_back_keyboard
from utils.logger import log_to_group

router = Router()

async def show_profile_with_back(callback: CallbackQuery, user_id: int, success_msg: str = ""):
    """
    Displays user profile with consistent error handling and back button
    """
    try:
        profile = await get_profile_data(user_id)
        if not profile:
            raise ValueError("Profile data not found in database")

        # Build profile message
        profile_text = [
            f"👤 <b>Your Profile</b>",
            f"🆔 <b>User ID:</b> <code>{user_id}</code>",
            f"💸 <b>Earnings:</b> ₹{profile.get('earnings', 0)}",
            f"👍 <b>Clicks:</b> {profile.get('clicks', 0)}",
            f"✅ <b>Approved:</b> {'Yes' if profile.get('approved', False) else 'No'}"
        ]

        # Add optional fields
        if profile.get('username') and profile['username'] != "NoUsername":
            profile_text.insert(2, f"📌 <b>Username:</b> @{profile['username']}")
        
        if profile.get('bot_link'):
            profile_text.append(f"🤖 <b>Bot Link:</b> {profile['bot_link']}")

        full_text = (f"{success_msg}\n\n" if success_msg else "") + "\n".join(profile_text)

        await callback.message.edit_text(
            full_text,
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )

    except TelegramBadRequest as e:
        error_msg = f"Message edit failed for user {user_id}: {str(e)}"
        print(error_msg)
        await log_to_group(callback.bot, f"⚠️ Profile Error\n{error_msg}")
        await callback.answer("Profile updated! Please refresh.", show_alert=True)
    except Exception as e:
        error_msg = f"Profile display error for user {user_id}: {str(e)}"
        print(error_msg)
        await log_to_group(callback.bot, f"⚠️ Profile Error\n{error_msg}")
        await callback.message.edit_text(
            "⚠️ <b>Failed to load profile</b>\nPlease try again later.",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    """
    Handles profile button clicks with registration checks
    """
    user = callback.from_user
    user_id = user.id
    
    try:
        # Clear existing keyboard
        try:
            await callback.message.edit_reply_markup(reply_markup=None)
        except:
            pass

        if not await is_registered_user(user_id):
            greeting = f"👋 Hello @{user.username}!" if user.username else f"👋 Hello {user.full_name}!"
            await callback.message.edit_text(
                f"{greeting}\n\n⚠️ <b>Registration required</b>\nClick below to join our network.",
                reply_markup=await get_register_keyboard(user_id),
                parse_mode="HTML"
            )
        else:
            await show_profile_with_back(callback, user_id)
            
    except Exception as e:
        error_msg = f"Profile callback error for user {user_id}: {str(e)}"
        print(error_msg)
        await log_to_group(callback.bot, f"⚠️ Profile Error\n{error_msg}")
        await callback.message.edit_text(
            "⚠️ <b>Service unavailable</b>\nPlease try again later.",
            parse_mode="HTML"
        )
    finally:
        await callback.answer()
