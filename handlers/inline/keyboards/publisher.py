from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_publisher_panel_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📊 Dashboard", callback_data="dashboard")],
        [InlineKeyboardButton("🤖 Bot Monetization", callback_data="bot_monetization")],
        [InlineKeyboardButton("💳 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton("◀️ Back", callback_data="go_back")]
    ])

def get_register_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("✅ Accept & Register", callback_data="register_accept")]
    ])
