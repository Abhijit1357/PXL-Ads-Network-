import asyncio
import os
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import start, publisher, advertiser, admin, earnings
from handlers.inline import general as inline_general  # NEW
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running..."

async def main():
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())

    # Register all handlers
    dp.include_routers(
        start.router,
        publisher.router,
        advertiser.router,
        admin.router,
        earnings.router,
        inline_general.router  # NEW INLINE ROUTER
    )

    # Set default commands
    await bot.set_my_commands([
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="help", description="How this bot works"),
        BotCommand(command="earnings", description="Check your earnings"),
        BotCommand(command="submit_ad", description="Submit an ad"),
        BotCommand(command="register_bot", description="Register your bot to earn")
    ])

    print("Bot is running...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    import threading

    # Start Flask app in a separate thread (for Koyeb or UptimeRobot pings)
    threading.Thread(
        target=lambda: app.run(
            host='0.0.0.0',
            port=int(os.environ.get("PORT", 5000)),
            use_reloader=False
        )
    ).start()

    # Start Telegram bot
    asyncio.run(main())
