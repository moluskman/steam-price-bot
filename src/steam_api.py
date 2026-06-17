import aiohttp
from typing import Optional


async def get_steam_game(app_id: int) -> Optional[dict]:
    url = f"https://store.steampowered.com/api/appdetails?appids={app_id}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                if data[str(app_id)]["success"]:
                    return data[str(app_id)]["data"]
    return None


def extract_price_info(game_data: dict) -> tuple:
    name = game_data.get("name")
    price_info = game_data.get("price_overview", {})
    initial_cents = price_info.get("initial", 0)
    original_price = initial_cents / 100.0
    return name, original_price


async def search_steam_game(
    game_name: str,
) -> int | None:  # Defines an asynchronous function
    """
    Searches steam for a game by name and returns the app ID of the first result, or None if not found.
    """
    url = "https://store.steampowered.com/api/storesearch/"
    params = {"term": game_name, "l": "english", "cc": "AU"}

    async with aiohttp.ClientSession() as session:
        try:  # Starts a block to safely test for code errors
            async with session.get(url, params=params) as response:
                if response.status == 200:  # Checks if a condition is met
                    data = await response.json()
                    items = data.get("items", [])

                if items:
                    top_result = items[0]
                    return top_result.get("id")

        except aiohttp.ClientError as e:  # Handles specific errors if they happen
            print(f"An error occurred while searching for the game: {e}")

    return None
