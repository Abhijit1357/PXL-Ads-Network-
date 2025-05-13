from aiogram import Router, types
from aiogram.filters import Command
from db.models import approve_ad, approve_publisher, approve_payment

router = Router()

ADMIN_IDS = [12345678]  # Add your Telegram ID here

@router.message(Command("approve_ad"))
async def approve_ad_cmd(msg: types.Message):
    if msg.from_user.id in ADMIN_IDS:
        try:
            ad_id = msg.text.split(maxsplit=1)[1]
            await approve_ad(ad_id)
            await msg.answer("Ad approved.")
        except IndexError:
            await msg.answer("Invalid format. Use /approve_ad ad_id")
    else:
        await msg.answer("Not authorized.")

@router.message(Command("approve_bot"))
async def approve_bot_cmd(msg: types.Message):
    if msg.from_user.id in ADMIN_IDS:
        try:
            uid = msg.text.split(maxsplit=1)[1]
            await approve_publisher(int(uid))
            await msg.answer("Bot approved.")
        except (IndexError, ValueError):
            await msg.answer("Invalid format. Use /approve_bot user_id")
    else:
        await msg.answer("Not authorized.")
