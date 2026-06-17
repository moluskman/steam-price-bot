import discord
from src.steam_api import get_steam_game, extract_price_info
from src.database import add_tracked_game


async def handle_commands(message: discord.Message):
    if message.content.startswith("!watch"):  # checks for command
        parts = message.content.split()  # splits the message into parts
        if len(parts) > 1:  # checks if there is an app id provided
            app_id = parts[1]  # gets the app id from the message
            try:
                game_id = int(app_id)  # converts the app id to an integer
                await message.channel.send(
                    f" Looking up Steam App ID: {game_id}..."
                )  # loading message
                game_data = await get_steam_game(
                    game_id
                )  # get game data from steam api
                if game_data:  # check if game data was found
                    name, original_price = extract_price_info(
                        game_data
                    )  # extract just the name and original price from the game data
                    is_new_game = add_tracked_game(game_id, name, original_price)
                    if is_new_game:
                        await message.channel.send(
                            f" Now watching **{name}**! Original Price: ${original_price:.2f}"
                        )
                    else:
                        await message.channel.send(f" I'm already watching **{name}**!")
                else:
                    await message.channel.send(
                        " Could not find that game on Steam. Double-check the ID!"
                    )
            except ValueError:  # if the app id is not a valid integer
                await message.channel.send(
                    " Please provide a valid Steam App ID.! Example: `!watch 570`"
                )
