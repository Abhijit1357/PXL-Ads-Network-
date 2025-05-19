from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.models import get_profile_data
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BotMonetizationKeyboards")

router = Router()

async def show_monetization_menu(user_id):
    profile = await get_profile_data(user_id)
    monetization_status = profile.get("monetization_status", "not_applied")

    if monetization_status == "not_applied":
        text = (
            "🤖 <b>Bot Monetization</b>\n\n"
            "You need to apply for monetization to start earning.\n"
            "Click below to apply!"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📝 Apply for Monetization", callback_data="apply_monetization")],
            [InlineKeyboardButton(text="◀️ Back", callback_data="publisher_panel")]
        ])
    elif monetization_status == "pending":
        text = (
            "🤖 <b>Bot Monetization</b>\n\n"
            "Your monetization application is pending.\n"
            "Please wait for admin approval."
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Back", callback_data="publisher_panel")]
        ])
    else:
        # User is approved for monetization
        text = (
            "🤖 <b>Bot Monetization</b>\n\n"
            "Choose an option to manage your monetization:"
        )
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="📜 View Bots", callback_data="view_bots")],
            [InlineKeyboardButton(text="➕ Add New Bot", callback_data="add_new_bot")],
            [InlineKeyboardButton(text="📊 Monetization Stats", callback_data="monetization_stats")],
            [InlineKeyboardButton(text="◀️ Back", callback_data="publisher_panel")]
        ])
    
    return text, keyboard

async def show_add_bot_menu(user_id):
    profile = await get_profile_data(user_id)
    pending_bots = profile.get("pending_bots", [])
    
    if pending_bots:
        pending_list = "\n".join([f"- {bot}" for bot in pending_bots])
        text = (
            "➕ <b>Add New Bot</b>\n\n"
            "You have pending bots:\n"
            f"{pending_list}\n\n"
            "Click below to add another bot."
        )
    else:
        text = (
            "➕ <b>Add New Bot</b>\n\n"
            "Click below to add a new bot for monetization."
        )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📝 Enter Bot Link", callback_data="enter_bot_link")],
        [InlineKeyboardButton(text="◀️ Back", callback_data="bot_monetization")]
    ])
    return text, keyboard
