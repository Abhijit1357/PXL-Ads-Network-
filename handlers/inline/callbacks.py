from aiogram import Router
from aiogram.types import CallbackQuery
from aiogram.filters import F

router = Router()

@router.callback_query(F.data == "publisher_panel")
async def publisher_panel_cb(callback: CallbackQuery):
    await callback.message.answer("📢 Publisher panel coming soon.")
    await callback.answer()

@router.callback_query(F.data == "advertiser_panel")
async def advertiser_panel_cb(callback: CallbackQuery):
    await callback.message.answer("💼 Advertiser panel coming soon.")
    await callback.answer()

@router.callback_query(F.data == "help")
async def help_cb(callback: CallbackQuery):
    await callback.message.answer("❓ Here's how the bot works...")
    await callback.answer()

@router.callback_query(F.data == "privacy")
async def privacy_cb(callback: CallbackQuery):
    await callback.message.answer("🔐 Your data is safe with us.")
    await callback.answer()
