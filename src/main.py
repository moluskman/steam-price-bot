import discord
import os
from dotenv import load_dotenv

# 1. Load the environment variables first!
load_dotenv()

# 2. Now it's safe to import your local files
from src.database import init_db
from src.commands import handle_commands
from src.scheduler import check_for_sales

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
