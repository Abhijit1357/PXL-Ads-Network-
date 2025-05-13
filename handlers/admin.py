from aiogram import Router, types
from db.models import approve_ad, approve_publisher, approve_payment

router = Router()

ADMIN_IDS = [12345678]  # Add your Telegram ID here

@router.message(commands=["approve_ad"])
async def approve_ad_cmd(msg: types.Message):
    if msg.from_user.id in ADMIN_IDS:
        ad_id = msg.text.split(maxsplit=1)[1]
        await approve_ad(ad_id)
        await msg.answer("Ad approved.")
    else:
        await msg.answer("Not authorized.")

@router.message(commands=["approve_bot"])
async def approve_bot_cmd(msg: types.Message):
    if msg.from_user.id in ADMIN_IDS:
        uid = msg.text.split(maxsplit=1)[1]
        await approve_publisher(int(uid))
        await msg.answer("Bot approved.")
