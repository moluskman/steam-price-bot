import os
import discord
from dotenv import load_dotenv

# 1. Load the environment variables first!
# Since main.py is inside /src, we look one folder up for the .env file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../.env"))

# 2. Now import your local files directly without 'src.'
from database import init_db
from commands import handle_commands
from scheduler import check_for_sales

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)


@client.event
async def on_ready():
    init_db()
    print("Jewvis Online")
    check_for_sales.start(client)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    await handle_commands(message)


client.run(os.getenv("DISCORD_BOT_TOKEN"))
