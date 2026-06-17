import discord
from discord.ext import tasks
import sqlite3
from src.steam_api import get_steam_game
import os

ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID"))
ALERT_ROLE_ID = int(os.getenv("ALERT_ROLE_ID"))


def get_all_tracked_games():
    """Fetches all tracked games from the database."""
    conn = sqlite3.connect("data/bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT app_id, name, original_price FROM tracked_games")
    games = cursor.fetchall()
    conn.close()
    return games


@tasks.loop(hours=24)
async def check_for_sales(client: discord.Client):
    await client.wait_until_ready()

    channel = client.get_channel(ALERT_CHANNEL_ID)
    if not channel:
        print(f"Error: Could not find channel with ID {ALERT_CHANNEL_ID}")
        return
    tracked_games = get_all_tracked_games()

    for app_id, name, original_price in tracked_games:
        game_data = await get_steam_game(app_id)
        if game_data:
            data_block = game_data.get("price_overview")
            if not data_block:
                continue

            current_price = data_block.get("final") / 100

            if current_price < original_price:
                discount_percent = int(
                    ((original_price - current_price) / original_price) * 100
                )

                await channel.send(
                    f"<@&{ALERT_ROLE_ID}> **{name}** is on sale! Original Price: ${original_price:.2f}, Current Price: ${current_price:.2f} ({discount_percent}% off)"
                )
