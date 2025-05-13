from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Publisher Panel", callback_data="publisher_panel"), InlineKeyboardButton(text="💼 Advertiser Panel", callback_data="advertiser_panel")],
        [InlineKeyboardButton(text="📣 Join Channel", url="https://t.me/PXL_Ads_Network"), InlineKeyboardButton(text="❓ Help", callback_data="help")],
        [InlineKeyboardButton(text="🔐 Privacy Policy", callback_data="privacy")],
    ])
    return keyboard
