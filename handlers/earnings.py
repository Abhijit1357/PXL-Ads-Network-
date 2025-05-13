from aiogram import Router, types
from db.models import get_earnings

router = Router()

@router.message(commands=["earnings"])
async def earnings(msg: types.Message):
    earnings_data = await get_earnings(msg.from_user.id)
    await msg.answer(f"You have earned ₹{earnings_data:.2f} so far.")
