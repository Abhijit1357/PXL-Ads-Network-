import asyncio
import os
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from config import BOT_TOKEN
from handlers import start, advertiser, admin, earnings
from handlers.inline.callbacks import inline_callbacks_router
from flask import Flask
from db.db import init_db  # Import your MongoDB init function

#Logging configuration
logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s:%(name)s:%(message)s"
)
logging.getLogger("aiogram.event").setLevel(logging.ERROR)

app = Flask(__name__)

@app.route('/')
def index():
    return "Bot is running..."

async def main():
    try:
        # Initialize MongoDB connection before starting bot
        await init_db()
        print("init_db function successfully completed")
        logging.info("Database initialized successfully")
    except Exception as e:
        print(f"Error in init_db function: {str(e)}")
        logging.error(f"Error initializing database: {str(e)}")

    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        start.router,
        advertiser.router,
        admin.router,
        earnings.router,
        inline_callbacks_router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
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
    # Run Flask app in a separate thread
    threading.Thread(
        target=lambda: app.run(
            host='0.0.0.0',
            port=int(os.environ.get("PORT", 5000)),
            use_reloader=False
        )
    ).start()
    # Run async bot main loop
    asyncio.run(main())
