from aiogram import Router
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from db.models import get_profile_data, apply_for_monetization, add_bot_for_approval, get_user_bots, get_stats
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("BotMonetizationCallbacks")

router = Router()

# FSM for handling bot link input
class BotLinkForm(StatesGroup):
    waiting_for_bot_link = State()

@router.callback_query(lambda x: x.data == "bot_monetization")
async def bot_monetization_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    text, keyboard = await show_monetization_menu(user_id)
    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda x: x.data == "apply_monetization")
async def apply_monetization_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    await apply_for_monetization(user_id)
    text, keyboard = await show_monetization_menu(user_id)
    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()
    logger.info(f"User {user_id} applied for monetization")

@router.callback_query(lambda x: x.data == "view_bots")
async def view_bots_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    bots = await get_user_bots(user_id)
    
    if not bots:
        text = "📜 <b>View Bots</b>\n\nYou have no bots. Add a bot to start monetizing!"
    else:
        total_bots = len(bots)
        bot_details = "\n\n".join([
            f"🤖 Bot: {bot['bot_link']}\n"
            f"Status: {bot['status']}\n"
            f"Ad Code: {bot['ad_code'] if bot['ad_code'] else 'N/A'}"
            for bot in bots
        ])
        text = (
            f"📜 <b>View Bots</b>\n\n"
            f"Total Bots: {total_bots}\n\n"
            f"{bot_details}"
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Back", callback_data="bot_monetization")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda x: x.data == "add_new_bot")
async def add_new_bot_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    text, keyboard = await show_add_bot_menu(user_id)
    await callback.message.edit_text(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(lambda x: x.data == "enter_bot_link")
async def enter_bot_link_cb(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "➕ <b>Add New Bot</b>\n\n"
        "Please enter your bot link below (e.g., https://t.me/MyBot):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Back", callback_data="add_new_bot")]
        ]),
        parse_mode="HTML"
    )
    await state.set_state(BotLinkForm.waiting_for_bot_link)
    await callback.answer()

@router.message(StateFilter(BotLinkForm.waiting_for_bot_link))
async def process_bot_link(message: Message, state: FSMContext):
    user_id = message.from_user.id
    bot_link = message.text.strip()
    
    if not bot_link.startswith("https://t.me/"):
        await message.reply(
            "⚠️ Invalid bot link. It should start with https://t.me/\n"
            "Please try again.",
            parse_mode="HTML"
        )
        return
    
    await add_bot_for_approval(user_id, bot_link)
    await message.reply(
        f"✅ Bot {bot_link} submitted for approval.\n"
        "Please wait for admin approval.",
        parse_mode="HTML"
    )
    logger.info(f"Bot {bot_link} submitted for approval by user {user_id}")
    
    # Reset state and show Add New Bot menu
    await state.clear()
    text, keyboard = await show_add_bot_menu(user_id)
    await message.reply(
        text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.callback_query(lambda x: x.data == "monetization_stats")
async def monetization_stats_cb(callback: CallbackQuery):
    user_id = callback.from_user.id
    stats = await get_stats(user_id)
    bots = await get_user_bots(user_id)
    
    if not stats or not bots:
        text = "📊 <b>Monetization Stats</b>\n\nNo stats available. Start monetizing your bots to see analytics!"
    else:
        stats_details = "\n\n".join([
            f"🤖 Bot: {bot['bot_link']}\n"
            f"Clicks: {stat['clicks']}"
            for bot, stat in [(b, s) for b in bots for s in stats if s['bot_id'] == b['bot_id']]
        ])
        text = (
            f"📊 <b>Monetization Stats</b>\n\n"
            f"{stats_details}"
        )
    
    await callback.message.edit_text(
        text,
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Back", callback_data="bot_monetization")]
        ]),
        parse_mode="HTML"
    )
    await callback.answer()
