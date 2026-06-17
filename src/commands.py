import discord
from database import add_tracked_game, get_watchlist, remove_tracked_game
from steam_api import extract_price_info, get_steam_game, search_steam_game


async def handle_commands(message: discord.Message):
    # !testalert command
    if message.content.startswith("!testalert"):
        from scheduler import check_for_sales

        await message.channel.send("Manually triggering a sales check...")
        # Bypasses the loop framework to run the core function right away for testing
        await check_for_sales.__wrapped__(message.guild.me.client)
        return

    # !watchlist command
    if message.content.startswith("!watchlist"):
        games = get_watchlist()
        if not games:
            await message.channel.send("Your watchlist is currently empty.")
            return
        embed = discord.Embed(title="Your Current Wishlist", color=discord.Color.blue())
        for app_id, name, original_price in games:
            embed.add_field(name=name, value=f"${original_price:.2f}", inline=False)
        await message.channel.send(embed=embed)
        return

    # !watch command
    if message.content.startswith("!watch"):
        command_arg = message.content[7:].strip()
        try:
            game_id = int(command_arg)
        except ValueError:
            game_id = await search_steam_game(command_arg)

        if not game_id:
            await message.channel.send(
                "Could not find that game on Steam. Double-check the name!"
            )
            return

        await message.channel.send(f"Looking up Steam App ID: {game_id}...")
        game_data = await get_steam_game(game_id)

        if game_data:
            name, original_price = extract_price_info(game_data)
            is_new_game = add_tracked_game(game_id, name, original_price)

            if is_new_game:
                embed = discord.Embed(
                    title="Now Tracking Game!",
                    description=f"Successfully added **{name}** to the watchlist.",
                    color=discord.Color.green(),
                )
                embed.add_field(name="Game Name", value=name, inline=True)
                embed.add_field(
                    name="Original Price",
                    value=f"${original_price:.2f}",
                    inline=True,
                )

                image_url = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{game_id}/header.jpg"
                embed.set_image(url=image_url)
                await message.channel.send(embed=embed)
            else:
                await message.channel.send(f"I'm already watching **{name}**!")
        else:
            await message.channel.send(
                "Could not find that game on Steam. Double-check the ID!"
            )
        return

    # !stopwatching command
    if message.content.startswith("!stopwatching"):
        command_arg = message.content[14:].strip()

        try:
            game_id = int(command_arg)
        except ValueError:
            game_id = await search_steam_game(command_arg)

        if not game_id:
            await message.channel.send(
                "Could not find that game on Steam. Double-check the name!"
            )
            return

        game_name = remove_tracked_game(game_id)
        if game_name:
            embed = discord.Embed(
                title="Stopped Watching Game",
                description=f"Successfully removed **{game_name}** from the watchlist.",
                color=discord.Color.red(),
            )
            image_url = f"https://shared.fastly.steamstatic.com/store_item_assets/steam/apps/{game_id}/header.jpg"
            embed.set_image(url=image_url)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send(
                f"I wasn't tracking a game with ID **{game_id}**."
            )
        return
