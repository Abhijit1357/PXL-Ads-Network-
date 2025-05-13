from aiogram import Router, types
from db.models import submit_ad, get_ad_stats

router = Router()

@router.message(commands=["submit_ad"])
async def submit_ad_cmd(msg: types.Message):
    # Example format: /submit_ad YourAdTextHere::TargetBots
    try:
        _, data = msg.text.split(maxsplit=1)
        text, bots = data.split("::")
        await submit_ad(msg.from_user.id, text.strip(), bots.strip().split(","))
        await msg.answer("Ad submitted for review.")
    except Exception:
        await msg.answer("Invalid format. Use /submit_ad Text::bot1,bot2")

@router.message(commands=["ad_stats"])
async def ad_stats(msg: types.Message):
    stats = await get_ad_stats(msg.from_user.id)
    await msg.answer(f"Your Ad Stats:\n\n{stats}")
