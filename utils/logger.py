from aiogram import Bot
from config import LOG_CHANNEL

async def log_to_group(bot: Bot, message: str):
    try:
        if LOG_CHANNEL:
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text=message,
                parse_mode="HTML"
            )
    except Exception as e:
        print(f"Failed to send log message: {e}")
