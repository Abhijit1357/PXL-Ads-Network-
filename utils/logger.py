from aiogram.bot import Bot
from config import LOG_GROUP_ID

async def log_to_group(bot: Bot, message: str):
    if LOG_GROUP_ID:
        try:
            await bot.send_message(LOG_GROUP_ID, message, parse_mode="HTML")
        except Exception as e:
            print(f"[Logger Error] {e}")
