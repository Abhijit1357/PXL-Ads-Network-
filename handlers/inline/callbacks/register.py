from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import create_profile_if_not_exists, is_registered_user
from utils.logger import log_to_group
from handlers.inline.keyboards import get_back_keyboard
from aiogram.exceptions import TelegramBadRequest

router = Router()

@router.callback_query(lambda c: c.data == "register_accept")
async def register_callback(callback: CallbackQuery):
    user = callback.from_user
    user_id = user.id
    username = user.username or "NoUsername"
    
    try:
        # Attempt to create profile and verify it was created
        profile_created = await create_profile_if_not_exists(user_id, username)
        
        if not profile_created:
            # Check if user is already registered
            if await is_registered_user(user_id):
                await callback.answer("You're already registered!", show_alert=True)
                return
            
            # If not created and not registered, show error
            await callback.message.edit_text(
                "⚠️ <b>Registration failed!</b>\nPlease try again later.",
                parse_mode="HTML"
            )
            await callback.answer()
            return

        # Log successful registration
        log_msg = (
            f"✅ New user registered!\n\n"
            f"🆔 <code>{user_id}</code>\n"
            f"👤 {'@' + username if username != 'NoUsername' else user.full_name}"
        )
        await log_to_group(callback.bot, log_msg)

        # Update message with success confirmation
        await callback.message.edit_text(
            "✅ <b>Registration successful!</b>\n\n"
            "You can now view your profile by clicking '👤 Profile'",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )

    except TelegramBadRequest as e:
        # Handle cases where message can't be edited
        print(f"Message edit error for user {user_id}: {e}")
        await callback.answer("Registration successful! Check your profile now.", show_alert=True)
    except Exception as e:
        print(f"Unexpected error during registration for user {user_id}: {e}")
        await callback.message.edit_text(
            "⚠️ <b>Registration failed due to technical error</b>\nOur team has been notified.",
            parse_mode="HTML"
        )
    finally:
        await callback.answer()
