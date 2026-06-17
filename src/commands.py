import discord
from src.steam_api import get_steam_game, extract_price_info, search_steam_game
from src.database import add_tracked_game, remove_tracked_game, get_watchlist


async def handle_commands(message: discord.Message):
    # watch command
    if message.content.startswith("!watchlist"):
        games = get_watchlist()
        if not games:
            await message.channel.send("Your watchlist is currently empty.")
            return
        embed = discord.Embed(title="Your Current Wishlist", color=discord.Color.blue())
        for app_id, name, original_price in games:
            embed.add_field(name=name, value=f"${original_price:.2f}", inline=False)
        await message.channel.send(embed=embed)
        return  # stops so it doesn't do !watch

    if message.content.startswith("!watch"):  # checks for command
        command_arg = message.content[
            7:
        ].strip()  # .strip() removes any accidental extra spaces at the start or end
        try:
            game_id = int(command_arg)  # converts the app id to an integer
        except ValueError:  # if the app id is not a valid integer
            game_id = await search_steam_game(command_arg)  # try searching by name

        if not game_id:
            await message.channel.send(
                " Could not find that game on Steam. Double-check the name!"
            )
            return

        await message.channel.send(f" Looking up Steam App ID: {game_id}...")
        game_data = await get_steam_game(game_id)  # get game data from steam api

        if game_data:  # check if game data was found
            name, original_price = extract_price_info(game_data)
            is_new_game = add_tracked_game(game_id, name, original_price)

            if is_new_game:
                # create discord embed to confirm command success with game details and image
                embed = discord.Embed(
                    title=" Now Tracking Game!",
                    description=f"Successfully added **{name}** to the watchlist.",
                    color=discord.Color.green(),  # Green border side bar
                )
                embed.add_field(name="Game Name", value=name, inline=True)
                embed.add_field(
                    name="Original Price",
                    value=f"${original_price:.2f}",
                    inline=True,
                )

                # Add the Steam header image
                image_url = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{game_id}/header.jpg"
                embed.set_image(url=image_url)

                # Send the embed instead of standard text
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f" I'm already watching **{name}**!")
        else:
            await message.channel.send(
                " Could not find that game on Steam. Double-check the ID!"
            )

    # stop watching command
    if message.content.startswith("!stopwatching"):
        command_arg = message.content[14:].strip()

        # find the ID
        try:
            game_id = int(command_arg)  # converts the app id to an integer
        except ValueError:  # if the app id is not a valid integer
            game_id = await search_steam_game(command_arg)  # try searching by name

        #  verify the ID exists
        if not game_id:
            await message.channel.send(
                " Could not find that game on Steam. Double-check the name!"
            )
            return

        # run the removal logic safely outside the try/except block
        game_name = remove_tracked_game(game_id)
        if game_name:
            embed = discord.Embed(
                title="Stopped Watching Game",
                description=f"Successfully removed **{game_name}** from the watchlist.",
                color=discord.Color.red(),  # red border bc removing it
            )
            image_url = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{game_id}/header.jpg"
            embed.set_image(url=image_url)
            await message.channel.send(embed=embed)
            return  # stops bot so it doesn't leak into other logic
        else:
            await message.channel.send(
                f"I wasn't tracking a game with ID **{game_id}**."
            )
            return
