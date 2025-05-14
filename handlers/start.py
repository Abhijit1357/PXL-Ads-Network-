from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from templates.info_texts import WELCOME_TEXT
from handlers.inline import get_start_keyboard

router = Router()

@router.message(Command("start"))
async def start_handler(msg: Message):
    keyboard = get_start_keyboard()
    await msg.answer(WELCOME_TEXT.format(name=msg.from_user.full_name), reply_markup=keyboard)
