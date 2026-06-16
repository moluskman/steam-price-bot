import discord
import os
from dotenv import load_dotenv
from src.database import init_db
from src.commands import handle_commands

# Load environment variables
load_dotenv()


intents = discord.Intents.default()


intents.message_content = True

# 3. Pass those intents into your client
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
