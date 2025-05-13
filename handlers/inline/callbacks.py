from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import F
from templates.info_texts import WELCOME_TEXT, PRIVACY_POLICY_TEXT

router = Router()

#Back button keyboard
def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Back", callback_data="go_back")]
    ])

@router.callback_query(F.data == "publisher_panel")
async def publisher_panel_cb(callback: CallbackQuery):
    await callback.message.edit_text(
        "📢 Publisher panel coming soon.",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "advertiser_panel")
async def advertiser_panel_cb(callback: CallbackQuery):
    await callback.message.edit_text(
        "💼 Advertiser panel coming soon.",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_cb(callback: CallbackQuery):
    await callback.message.edit_text(
        "❓ Here's how the bot works...",
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "privacy")
async def privacy_cb(callback: CallbackQuery):
    await callback.message.edit_text(
        PRIVACY_POLICY_TEXT,
        reply_markup=get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "go_back")
async def go_back(callback: CallbackQuery):
    from handlers.inline.general import get_start_keyboard  # import inside to avoid circular import
    await callback.message.edit_text(
        WELCOME_TEXT.format(name=callback.from_user.full_name),
        reply_markup=get_start_keyboard()
    )
    await callback.answer()
