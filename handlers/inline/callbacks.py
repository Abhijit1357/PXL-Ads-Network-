from aiogram.types import CallbackQuery

@router.callback_query(lambda c: c.data == "publisher_panel")
async def publisher_panel_cb(callback: CallbackQuery):
    await callback.message.answer("📢 Publisher panel coming soon.")
    await callback.answer()

@router.callback_query(lambda c: c.data == "advertiser_panel")
async def advertiser_panel_cb(callback: CallbackQuery):
    await callback.message.answer("💼 Advertiser panel coming soon.")
    await callback.answer()

@router.callback_query(lambda c: c.data == "help")
async def help_cb(callback: CallbackQuery):
    await callback.message.answer("❓ Here's how the bot works...")
    await callback.answer()

@router.callback_query(lambda c: c.data == "privacy")
async def privacy_cb(callback: CallbackQuery):
    await callback.message.answer("🔐 Your data is safe with us.")
    await callback.answer()
