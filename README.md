PXL Ads Network

PXL Ads Network is a custom Telegram Ads Network where publishers can earn by showing ads in their bots, and advertisers can promote their bots or services via short text ads.


---

Features

Publisher System: Bot owners can register and get monetized.

Advertiser Panel: Advertisers can submit text ads and track performance.

Admin Dashboard: Approve ads, bots, and process payouts.

Text Ads API (SDK): External bots can easily fetch and show ads.

CPM Based Earnings: Track views and income per 1000 impressions.



---

Folder Structure

project_root/
├── ad_bot/
│   ├── bot.py
│   ├── config.py
│   ├── handlers/
│   ├── utils/
│   ├── db/
│   ├── templates/
│   └── requirements.txt
├── sdk/
├── campaigns/
└── README.md


---

Installation

1. Clone the Repo



git clone https://github.com/yourusername/pxl-ads-network.git
cd pxl-ads-network

2. Install Requirements



pip install -r ad_bot/requirements.txt

3. Set Environment Variables in config.py



BOT_TOKEN = "your_telegram_bot_token"
MONGO_URI = "your_mongodb_connection"
LOG_CHANNEL_ID = -100xxxxxxxxx

4. Start the Bot



cd ad_bot
python bot.py


---

How It Works

Publishers: Register with their Telegram bot.

Advertisers: Submit short text ads with budget and CPM.

Ads: Delivered via API (sdk/fetch_ad.py) to other bots.

Earnings: Calculated based on ad views (CPM).



---

SDK for Other Bots

from sdk.fetch_ad import get_ad

ad_text = get_ad(publisher_id="your_bot_id")
await message.reply(ad_text)


---

Contribution

Pull requests are welcome. For major changes, please open an issue first.


---

License

This project is licensed under the MIT License.

