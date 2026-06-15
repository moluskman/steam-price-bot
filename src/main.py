import discord  # imports
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()  # Bot permissions and intents
intents.message_content = True
client = discord.Client(intents=intents)


@client.event  # Event listener for when the bot is ready
async def on_ready():
    print("Jewvis Online")


client.run(
    os.getenv("DISCORD_BOT_TOKEN")
)  # Grabs bot token from env file and runs the bot
