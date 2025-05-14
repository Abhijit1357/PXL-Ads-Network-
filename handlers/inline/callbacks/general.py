from aiogram import Router, F
from aiogram.types import CallbackQuery
import handlers.inline.keyboards as keyboards
from templates.info_texts import WELCOME_TEXT, PRIVACY_POLICY_TEXT

router = Router()

@router.callback_query(F.data == "help")
async def help_cb(callback: CallbackQuery):
    await callback.message.edit_text(
        "❓ Here's how the bot works...",
        reply_markup=keyboards.get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "privacy")
async def privacy_cb(callback: CallbackQuery):
    await callback.message.edit_text(
        PRIVACY_POLICY_TEXT,
        reply_markup=keyboards.get_back_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "go_back")
async def go_back(callback: CallbackQuery):
    await callback.message.edit_text(
        WELCOME_TEXT.format(name=callback.from_user.full_name),
        reply_markup=keyboards.get_start_keyboard()
    )
    await callback.answer()
