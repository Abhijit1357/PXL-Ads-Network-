from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from db.models import create_profile_if_not_exists, is_registered_user
from utils.logger import log_to_group
from handlers.inline.keyboards import get_back_keyboard
from datetime import datetime
import traceback
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.callback_query(lambda c: c.data == "register_accept")
async def register_callback(callback: CallbackQuery):
    user = callback.from_user
    registration_success = False
    error_details = ""
    
    try:
        logger.info(f"Registration attempt started for user {user.id}")
        
        # Attempt registration with detailed logging
        registration_success = await create_profile_if_not_exists(
            user.id,
            user.username or user.first_name
        )
        
        if not registration_success:
            # Check if already registered
            if await is_registered_user(user.id):
                msg = "✅ You're already registered!"
                await callback.answer(msg, show_alert=True)
                logger.info(f"User {user.id} attempted duplicate registration")
                return
                
            error_msg = "⚠️ <b>Registration failed!</b>\nPlease try again in a few minutes."
            error_details = "Registration failed without exception"
            await callback.message.edit_text(
                error_msg,
                parse_mode="HTML"
            )
            logger.warning(f"Registration failed silently for user {user.id}")
            return

        # Success case
        success_msg = "✅ <b>Registration successful!</b>"
        await callback.message.edit_text(
            f"{success_msg}\n\n"
            "You can now:\n"
            "- View your profile 👤\n"
            "- Submit ads 📢\n"
            "- Earn money 💰",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        
        logger.info(f"Successful registration for user {user.id}")
        registration_success = True

    except TelegramBadRequest as e:
        error_details = f"TelegramBadRequest: {str(e)}"
        await callback.answer(
            "Registration successful! Please check your profile.",
            show_alert=True
        )
        logger.info(f"Message edit failed but registration succeeded for {user.id}")

    except Exception as e:
        error_details = f"{type(e).__name__}: {str(e)}\n{traceback.format_exc()}"
        error_msg = "⚠️ <b>Technical error occurred</b>\nOur team has been notified."
        await callback.message.edit_text(
            error_msg,
            parse_mode="HTML"
        )
        logger.error(f"Critical registration error for {user.id}: {error_details}")

    finally:
        # Detailed error reporting to your log group
        if not registration_success and error_details:
            await log_to_group(
                f"🚨 REGISTRATION FAILED\n"
                f"User ID: {user.id}\n"
                f"Username: @{user.username if user.username else 'N/A'}\n"
                f"Time: {datetime.utcnow().isoformat()}\n"
                f"Error Details:\n{error_details}"
            )
        
        # Success logging
        if registration_success:
            await log_to_group(
                f"✅ NEW REGISTRATION\n"
                f"ID: {user.id}\n"
                f"Name: {user.full_name}\n"
                f"Username: @{user.username if user.username else 'N/A'}\n"
                f"Time: {datetime.utcnow().isoformat()}"
            )
        
        await callback.answer()
