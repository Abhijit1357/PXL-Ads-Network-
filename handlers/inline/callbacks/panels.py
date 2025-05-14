from aiogram import Router, F
from aiogram.types import CallbackQuery
from handlers.inline.keyboards import get_back_keyboard

router = Router()

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
