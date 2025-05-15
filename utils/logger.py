from aiogram import Bot
from config import LOG_CHANNEL

async def log_to_group(bot: Bot, message: str):
    if LOG_CHANNEL:
        try:
            await bot.send_message(LOG_CHANNEL, message, parse_mode="HTML")
        except Exception as e:
            print(f"[Logger Error] {e}")
