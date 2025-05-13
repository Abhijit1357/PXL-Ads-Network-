from db.models import get_random_ad

# This function fetches a random approved ad
async def fetch_ad(bot_username: str) -> str:
    ad = await get_random_ad(bot_username)
    if not ad:
        return ""
    return f"Sponsored:\n\n{ad['text']}\n\n— via PXL Ads Network"
