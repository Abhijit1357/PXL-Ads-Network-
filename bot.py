# ad_bot/bot.py

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from handlers import start, publisher, advertiser, admin, earnings

async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    # Register all handlers
    dp.include_routers(
        start.router,
        publisher.router,
        advertiser.router,
        admin.router,
        earnings.router
    )

    # Set default commands
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="How this bot works"),
        BotCommand(command="earn", description="Check your earnings"),
        BotCommand(command="submit_ad", description="Submit an ad"),
        BotCommand(command="register_bot", description="Register your bot to earn")
    ])

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
