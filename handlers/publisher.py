from aiogram import Router, types
from aiogram.filters import Command
from db.models import register_publisher, check_eligibility
from templates.info_texts import ELIGIBLE_TEXT, NOT_ELIGIBLE_TEXT

router = Router()

@router.message(Command("register"))
async def register_bot(msg: types.Message):
    try:
        await register_publisher(msg.from_user.id, msg.from_user.username, "bot_link")
        await msg.answer("Registered successfully!")
    except Exception as e:
        await msg.answer("You are already registered or an error occurred.")
        print(f"Error: {e}")

@router.message(Command("eligibility"))
async def check(msg: types.Message):
    try:
        is_eligible = await check_eligibility(msg.from_user.id)
        await msg.answer(ELIGIBLE_TEXT if is_eligible else NOT_ELIGIBLE_TEXT)
    except Exception as e:
        await msg.answer("An error occurred.")
        print(f"Error: {e}")
