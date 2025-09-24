import os

import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()
mcp = FastMCP("riot")
base_url = "https://americas.api.riotgames.com"


async def make_riot_request(url: str):
    headers = {"X-Riot-Token": os.getenv("RIOT_API_KEY")}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


async def get_puuid_by_summoner(summoner_name: str, summoner_tagline: str) -> str:
    """Get the puuid of a summoner by summoner name and tagline

    Args:
        summoner_name: Summoner Name
        summoner_tagline: Summoner Tagline
    """
    url = f"{base_url}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{summoner_tagline}"
    response = await make_riot_request(url)
    return response["puuid"]


@mcp.tool()
async def get_matches_by_summoner(summoner_name: str, summoner_tagline: str) -> dict:
    puuid = await get_puuid_by_summoner(summoner_name, summoner_tagline)
    url = f"{base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    return await make_riot_request(url)


@mcp.tool()
async def get_match_details(match_id: str) -> dict:
    url = f"{base_url}/lol/match/v5/matches/{match_id}"
    return await make_riot_request(url)


@mcp.tool()
async def get_match_timeline(match_id: str) -> dict:
    url = f"{base_url}/lol/match/v5/matches/{match_id}/timeline"
    return await make_riot_request(url)


if __name__ == "__main__":
    mcp.run(transport="stdio")
