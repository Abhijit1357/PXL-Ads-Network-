from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from db.models import get_profile_data
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("Dashboard")

router = Router()

@router.callback_query(lambda x: x.data == "dashboard")
async def dashboard_cb(callback: CallbackQuery):
    try:
        user_id = callback.from_user.id
        # Fetch user profile data
        profile = await get_profile_data(user_id)
        if not profile:
            await callback.message.edit_text(
                "⚠️ Unable to fetch your profile data. Please try again later.",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="◀️ Back", callback_data="publisher_panel")]
                ]),
                parse_mode="HTML"
            )
            await callback.answer()
            return

        # Prepare dashboard message
        dashboard_text = (
            "📊 <b>Your Dashboard</b>\n\n"
            f"👤 <b>Username</b>: {callback.from_user.username or 'N/A'}\n"
            f"💰 <b>Earnings</b>: ₹{profile['earnings']}\n"
            f"👆 <b>Clicks</b>: {profile['clicks']}\n"
            f"✅ <b>Approved</b>: {'Yes' if profile['approved'] else 'No'}\n"
            f"🤖 <b>Bot Link</b>: {profile['bot_link'] or 'Not set'}\n\n"
            "Choose an option below:"
        )

        # Create keyboard with "Back" button
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Back", callback_data="publisher_panel")]
        ])

        # Edit message to show dashboard
        await callback.message.edit_text(
            dashboard_text,
            reply_markup=keyboard,
            parse_mode="HTML"
        )
        await callback.answer()
        logger.info(f"Dashboard shown to user {user_id}")
    except Exception as e:
        logger.error(f"Error showing dashboard for user {user_id}: {e}")
        await callback.message.edit_text(
            "⚠️ Error fetching dashboard. Please try again later.",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="◀️ Back", callback_data="publisher_panel")]
            ]),
            parse_mode="HTML"
        )
        await callback.answer()
