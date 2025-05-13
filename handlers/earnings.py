from aiogram import Router, types
from aiogram.filters import Command
from db.models import get_earnings

router = Router()

@router.message(Command("earnings"))
async def earnings(msg: types.Message):
    try:
        earnings_data = await get_earnings(msg.from_user.id)
        await msg.answer(f"Your earnings: ₹{earnings_data}")
    except Exception as e:
        await msg.answer("Error occurred while fetching earnings")
        print(f"Error: {e}")
