from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import register_publisher, get_profile_data, is_registered_user
import handlers.inline.keyboards as keyboards

router = Router()

async def show_profile_with_back(callback: CallbackQuery, user_id: int, success_message: str = ""):
    """Profile dikhane ka common function"""
    profile = await get_profile_data(user_id)
    text = (
        f"{success_message}\n\n" if success_message else "" +
        f"👤 <b>Your Profile</b>\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"💸 <b>Earnings:</b> ₹{profile['earnings']}\n"
        f"👍 <b>Clicks:</b> {profile['clicks']}\n"
        f"✅ <b>Approved:</b> {'Yes' if profile['approved'] else 'No'}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=keyboards.get_back_keyboard(),  # Yahi go_back wala keyboard use karega
        parse_mode="HTML"
    )

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id

    if not await is_registered_user(user_id):
        await callback.message.edit_text(
            "⚠️ <b>You are not registered.</b>\nPlease register first.",
            reply_markup=keyboards.get_register_keyboard(),
            parse_mode="HTML"
        )
    else:
        await show_profile_with_back(callback, user_id)
    await callback.answer()

@router.callback_query(lambda x: x.data == "register")
async def register_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    username = callback.from_user.username or ""

    if await is_registered_user(user_id):
        await callback.answer("You are already registered.", show_alert=True)
        return

    await register_publisher(user_id, username)

    await callback.message.edit_text(
        "✅ <b>Registration successful!</b>",
        reply_markup=keyboards.get_back_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer("Registered Successfully!")
