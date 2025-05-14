from aiogram import Router
from aiogram.types import CallbackQuery
from handlers.inline import keyboards

router = Router()

@router.callback_query(lambda x: x.data == "publisher_panel")
async def publisher_panel_cb(callback: CallbackQuery):
    keyboard = keyboards.get_publisher_panel_keyboard()
    text = """Publisher Panel"""
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()
