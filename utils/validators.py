import random

# Dummy bot checker — In production, use Bot API or manually verify
async def is_valid_bot(bot_username: str) -> bool:
    return bot_username.startswith("@") and len(bot_username) > 5

# CPM logic — ₹4 to ₹15 per 1,000 clicks depending on quality
async def calculate_cpm(score: int = None) -> int:
    if score is None:
        score = random.randint(1, 100)
    if score > 90:
        return 15
    elif score > 75:
        return 10
    elif score > 50:
        return 7
    else:
        return 4
