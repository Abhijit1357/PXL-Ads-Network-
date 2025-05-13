import requests

API_URL = "https://your-api-domain.com/get_ad"

def get_ad(bot_id):
    try:
        response = requests.get(API_URL, params={"bot_id": bot_id})
        if response.status_code == 200:
            ad_data = response.json()
            return ad_data.get("text", "")
        return ""
    except Exception as e:
        print(f"Failed to fetch ad: {e}")
        return ""
