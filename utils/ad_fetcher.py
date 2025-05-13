from db.models import get_random_ad

async def fetch_ad(bot_username: str) -> str:
    try:
        ad = await get_random_ad(bot_username)
        if not ad:
            return ""
        return f"Sponsored:\n\n{ad['text']}\n\n— via PXL Ads Network"
    except Exception as e:
        print(f"Error: {e}")
        return ""
