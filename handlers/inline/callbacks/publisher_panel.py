from aiogram import Router
from aiogram.types import CallbackQuery
from handlers.inline.keyboards import get_publisher_panel_keyboard, get_register_keyboard
from db.models import is_registered_user, create_profile_if_not_exists

router = Router()

@router.callback_query(lambda x: x.data == "publisher_panel")
async def publisher_panel_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    await create_profile_if_not_exists(user_id, username)
    if not await is_registered_user(user_id):
        await callback.message.edit_text(
            "⚠️ You are not registered yet.\nPlease accept the Privacy Policy to continue.",
            reply_markup=get_register_keyboard(user_id=callback.from_user.id),
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            "👤 <b>Your Publisher Panel</b>\nChoose an option below:",
            reply_markup=get_publisher_panel_keyboard(),
            parse_mode="HTML"
        )
    await callback.answer()
