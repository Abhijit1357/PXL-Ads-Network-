from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import get_profile_data, is_registered_user, create_profile_if_not_exists
from handlers.inline.keyboards import get_back_keyboard
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    await create_profile_if_not_exists(user_id, username)
    profile = await get_profile_data(user_id)
    if profile is not None:
        text = f""" 👤 <b>Your Profile</b> 🆔 User ID: <code>{user_id}</code> 💰 Total Earnings: ₹{profile.get('earnings', 0)} """
        await callback.message.edit_text(
            text,
            reply_markup=get_back_keyboard(),
            parse_mode="HTML"
        )
    else:
        await callback.message.edit_text(
            "⚠️ Profile data not found.",
            reply_markup=get_back_keyboard()
        )
    await callback.answer()

@router.callback_query(lambda x: x.data == "register_accept")
async def register_accept_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username
    await create_profile_if_not_exists(user_id, username)
    await callback.message.edit_text(
        "✅ Registration completed and Privacy Policy accepted.\nNow you can view your profile.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="👤 View Profile", callback_data="profile")]
        ])
    )
    await callback.answer()
