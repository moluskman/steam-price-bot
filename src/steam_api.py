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
