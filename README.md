# Steam Price Tracking Bot



A Discord bot that monitors a custom watchlist of Steam games and automatically pings a specific server role when a game goes on sale.

## Features
* **Live Price Monitoring:** Fetches real-time price data from the Steam API.
* **Role Pings:** Mentions a target server role automatically when a discount is found.
* **Database Tracking:** Stores tracked game details locally using SQLite.
* **Secure Configuration:** Environment variables keep secret tokens out of the codebase.

## Setup
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Create a `.env` file in the root directory with the following variables:
   ```text
   DISCORD_BOT_TOKEN=your_bot_token_here
   ALERT_CHANNEL_ID=your_channel_id
   ALERT_ROLE_ID=your_role_id'''
4.**Run the bot: python src/main.py**

