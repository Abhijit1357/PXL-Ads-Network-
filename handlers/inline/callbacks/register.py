from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest
from db.models import create_profile_if_not_exists, is_registered_user
from utils.logger import log_to_group
from handlers.inline.keyboards import get_back_keyboard

router = Router()

@router.callback_query(lambda c: c.data == "register_accept")
async def register_callback(callback: CallbackQuery):
    user = callback.from_user
    try:
        # Attempt registration
        success = await create_profile_if_not_exists(
            user.id,
            user.username or user.first_name
        )
        
        if not success:
            if await is_registered_user(user.id):
                await callback.answer(
                    "✅ You're already registered!",
                    show_alert=True
                )
                return
                
            await callback.message.edit_text(
                "⚠️ <b>Registration failed!</b>\n"
                "Please try again in a few minutes.",
                parse_mode="HTML"
            )
            await log_to_group(
                f"❌ Registration failed\n"
                f"User: {user.id}\n"
                f"Name: {user.full_name}"
            )
            return

        # Success case
        await callback.message.edit_text(
            "✅ <b>Registration successful!</b>\n\n"
            "You can now:\n"
            "- View your profile 👤\n"
            "- Submit ads 📢\n"
            "- Earn money 💰",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        
        await log_to_group(
            f"✅ New registration\n"
            f"ID: {user.id}\n"
            f"Name: {user.full_name}\n"
            f"Username: @{user.username}" if user.username else ""
        )

    except TelegramBadRequest:
        await callback.answer(
            "Registration successful! Please check your profile.",
            show_alert=True
        )
    except Exception as e:
        await callback.message.edit_text(
            "⚠️ <b>Technical error occurred</b>\n"
            "Our team has been notified.",
            parse_mode="HTML"
        )
        await log_to_group(
            f"🚨 CRITICAL REGISTRATION ERROR\n"
            f"User: {user.id}\n"
            f"Error: {str(e)}"
        )
    finally:
        await callback.answer()
