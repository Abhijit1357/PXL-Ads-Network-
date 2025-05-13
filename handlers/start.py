from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from templates.info_texts import WELCOME_TEXT

router = Router()

@router.message(Command(commands=["start", "help"]))
async def start_handler(msg: Message):
    await msg.answer(WELCOME_TEXT.format(name=msg.from_user.full_name))
