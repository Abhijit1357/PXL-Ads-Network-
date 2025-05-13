from aiogram import types, Router
from aiogram.types import Message
from templates.info_texts import WELCOME_TEXT

router = Router()

@router.message(commands=["start", "help"])
async def start_handler(msg: Message):
    await msg.answer(WELCOME_TEXT.format(name=msg.from_user.full_name))
