import discord
from discord.ext import tasks
import sqlite3
from src.steam_api import get_steam_game

import os

ALERT_CHANNEL_ID = int(os.getenv("ALERT_CHANNEL_ID"))


def get_all_tracked_games():
    """Fetches all tracked games from the database."""
    conn = sqlite3.connect("data/bot.db")
    cursor = conn.cursor()
    cursor.execute("SELECT app_id, name, original_price FROM tracked_games")
    games = cursor.fetchall()
    conn.close()
    return games


@tasks.loop(hours=24)  # runs once every 24 hours
async def check_for_sales(client: discord.Client):
    await client.wait_until_ready()  # wait until the bot is ready

    channel = client.get_channel(ALERT_CHANNEL_ID)  # get the channel to send alerts to
    if not channel:
        print(f"Error: Could not find channel with ID {ALERT_CHANNEL_ID}")
        return
    tracked_games = get_all_tracked_games()  # get all tracked games from the database

    for app_id, name, original_price in tracked_games:
        game_data = await get_steam_game(
            app_id
        )  # get the latest game data from the Steam API
        if game_data:
            data_block = game_data.get("price_overview", {})
            current_price = (
                data_block.get("final", original_price * 100) / 100
            )  # convert from cents to dollars
            discount_percent = data_block.get("discount_percent", 0)
            if discount_percent > 0 and current_price < original_price:
                await channel.send(
                    f"**{name}** is on sale! Original Price: ${original_price:.2f}, Current Price: ${current_price:.2f} ({discount_percent}% off)"
                )
