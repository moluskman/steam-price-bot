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
