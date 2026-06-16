import discord  # imports
import os
from src.commands import (
    handle_commands,
)  # import from commands file allowing 2 files to talk to each other
from dotenv import load_dotenv
from src.database import (
    init_db,
)  # import from database file allowing 2 files to talk to each other

load_dotenv()

intents = discord.Intents.default()  # Bot permissions and intents
intents.message_content = True
client = discord.Client(intents=intents)


@client.event  # Event listener for when the bot is ready
async def on_ready():
    init_db()  # Initializes the database when the bot is ready
    print("Jewvis Online")


@client.event
async def on_message(message):
    if (
        message.author == client.user
    ):  # Ignore messsages sent by the bot itself to prevent infinite loops
        return
    await handle_commands(
        message
    )  # Pass the message to command system to look for !watch command and handle it accordingly


client.run(
    os.getenv("DISCORD_BOT_TOKEN")
)  # Grabs bot token from env file and runs the bot
