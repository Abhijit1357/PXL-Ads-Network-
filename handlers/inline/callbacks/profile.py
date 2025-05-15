from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import register_publisher, get_profile_data, is_registered_user
import handlers.inline.keyboards as keyboards

router = Router()

async def show_profile_with_back(callback: CallbackQuery, user_id: int, success_message: str = ""):
    """Profile dikhane ka common function"""
    profile = await get_profile_data(user_id)
    text = (
        (f"{success_message}\n\n" if success_message else "") +  # Parentheses added here
        f"👤 <b>Your Profile</b>\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"💸 <b>Earnings:</b> ₹{profile['earnings']}\n"
        f"👍 <b>Clicks:</b> {profile['clicks']}\n"
        f"✅ <b>Approved:</b> {'Yes' if profile['approved'] else 'No'}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=keyboards.get_back_keyboard(),  # Back button keyboard
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
    try:
        user_id = callback.from_user.id
        username = callback.from_user.username or ""

        # Check registration status first
        if await is_registered_user(user_id):
            if "already registered" not in callback.message.text:  # Prevent duplicate alerts
                await callback.answer("✓ You're already registered", show_alert=True)
            return

        # Perform registration
        await register_publisher(user_id, username)
        
        # Build success message with profile
        profile_text = (
            "✅ <b>Registration Successful!</b>\n\n"
            f"👤 <b>Your Profile</b>\n"
            f"🆔 ID: <code>{user_id}</code>\n"
            f"💸 Earnings: ₹{(await get_profile_data(user_id))['earnings']}"
        )
        
        # Only edit if content changed
        if profile_text != callback.message.text:
            await callback.message.edit_text(
                profile_text,
                reply_markup=keyboards.get_back_keyboard(),
                parse_mode="HTML"
            )

        await callback.answer("🎉 Registration complete!")

    except Exception as e:
        print(f"Registration Error: {e}")
        await callback.answer("⚠️ Registration failed. Please try again.", show_alert=True)
