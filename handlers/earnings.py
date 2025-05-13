from aiogram import Router, types
from aiogram.filters import Command
from db.models import get_earnings

router = Router()

@router.message(Command("earnings"))
async def earnings(msg: types.Message):
    earnings_data = await get_earnings(msg.from_user.id)
    await msg.answer(f"Your earnings: ₹{earnings_data}")
