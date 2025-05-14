from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_publisher_panel_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 Dashboard", callback_data="dashboard")],
        [InlineKeyboardButton(text="🤖 Bot Monetization", callback_data="bot_monetization")],
        [InlineKeyboardButton(text="💳 Withdraw", callback_data="withdraw")],
        [InlineKeyboardButton(text="◀️ Back", callback_data="go_back")]
    ])
    return keyboard
