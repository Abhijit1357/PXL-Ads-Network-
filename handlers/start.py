from aiogram import types, Router
from aiogram.types import Message
from templates.info_texts import WELCOME_TEXT

router = Router()

# Use a filter to check if the message text is "start" or "help"
@router.message(lambda message: message.text.lower() in ["start", "help"])
async def start_handler(msg: Message):
    await msg.answer(WELCOME_TEXT.format(name=msg.from_user.full_name))
