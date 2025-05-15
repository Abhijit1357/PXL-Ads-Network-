from aiogram import Router
from aiogram.types import CallbackQuery
from db.models import register_publisher, get_profile_data, is_registered_user
import handlers.inline.keyboards as keyboards

router = Router()

async def show_profile_with_back(callback: CallbackQuery, user_id: int, success_msg: str = ""):
    #"""Fixed version with proper string concatenation and back button"""
    profile = await get_profile_data(user_id)
    # Fixed string concatenation with proper parentheses
    text = (
        (f"{success_msg}\n\n" if success_msg else "") +  
        f"👤 <b>Your Profile</b>\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"💸 <b>Earnings:</b> ₹{profile['earnings']}\n"
        f"👍 <b>Clicks:</b> {profile['clicks']}\n"
        f"✅ <b>Approved:</b> {'Yes' if profile['approved'] else 'No'}"
    )
    await callback.message.edit_text(
        text,
        reply_markup=keyboards.get_back_keyboard(),  # Back button guaranteed
        parse_mode="HTML"
    )

@router.callback_query(lambda x: x.data == "profile")
async def profile_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    if not await is_registered_user(user_id):
        await callback.message.edit_text(
            "⚠️ <b>Register First</b>\nClick Register to continue",
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
        
        # Check if already registered
        if await is_registered_user(user_id):
            await show_profile_with_back(callback, user_id)
            await callback.answer("✓ You're already registered")
            return
            
        # Process new registration
        await register_publisher(user_id, username)
        await show_profile_with_back(
            callback, 
            user_id,
            "✅ <b>Registration Successful!</b>"
        )
        await callback.answer("🎉 Welcome!")
        
    except Exception as e:
        print(f"Registration Error: {e}")
        await callback.answer("⚠️ Registration failed. Please try again.", show_alert=True)
