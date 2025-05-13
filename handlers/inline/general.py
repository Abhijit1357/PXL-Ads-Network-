from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from templates.info_texts import WELCOME_TEXT

router = Router()

@router.message(commands=["start"])
async def start_handler(msg: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📢 Publisher Panel", callback_data="publisher_panel")],
        [InlineKeyboardButton(text="💼 Advertiser Panel", callback_data="advertiser_panel")],
        [InlineKeyboardButton(text="📣 Join Channel", url="https://t.me/PXL_Ads_Network")],
        [InlineKeyboardButton(text="❓ Help", callback_data="help")],
        [InlineKeyboardButton(text="🔐 Privacy Policy", callback_data="privacy")],
    ])
    await msg.answer(WELCOME_TEXT.format(name=msg.from_user.full_name), reply_markup=keyboard)
