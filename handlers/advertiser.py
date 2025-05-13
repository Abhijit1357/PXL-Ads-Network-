from aiogram import Router, types
from aiogram.filters import Command
from db.models import submit_ad, get_ad_stats

router = Router()

@router.message(Command("submit_ad"))
async def submit_ad_cmd(msg: types.Message):
    # Example format: /submit_ad YourAdTextHere::TargetLink
    try:
        _, data = msg.text.split(maxsplit=1)
        text, link = data.split("::")
        await submit_ad(msg.from_user.id, text.strip(), link.strip())
        await msg.answer("Ad submitted for review.")
    except Exception:
        await msg.answer("Invalid format. Use /submit_ad Text::Link")

@router.message(Command("ad_stats"))
async def ad_stats(msg: types.Message):
    # You might need to adjust this to get ad stats by user ID or ad ID
    # For now, let's assume get_ad_stats function is adjusted accordingly
    stats = await get_ad_stats(msg.from_user.id)
    await msg.answer(f"Your Ad Stats:\n\n{stats}")
