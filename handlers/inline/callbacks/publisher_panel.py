from aiogram import Router
from aiogram.types import CallbackQuery
from handlers.inline.keyboards.publisher import get_publisher_panel_keyboard
from handlers.inline.keyboards.register import get_register_keyboard
from db.models import is_registered_user

router = Router()

@router.callback_query(lambda x: x.data == "publisher_panel")
async def publisher_panel_cb(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        if not await is_registered_user(user_id):
            await callback.message.edit_text(
                "⚠️ You are not registered yet.\nPlease accept the Privacy Policy to continue.",
                reply_markup=get_register_keyboard(),
                parse_mode="HTML"
            )
        else:
            await callback.message.edit_text(
                "👤 <b>Your Publisher Panel</b>\nChoose an option below:",
                reply_markup=get_publisher_panel_keyboard(),
                parse_mode="HTML"
            )
        await callback.answer()

    except Exception as e:
        print(f"Publisher Panel Error: {e}")
        await callback.message.edit_text(
            "⚠️ <b>Failed to load publisher panel.</b>\nPlease try again.",
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("⚠️ Error occurred.", show_alert=True)
