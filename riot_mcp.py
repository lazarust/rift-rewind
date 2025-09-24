import os

import httpx
from dotenv import load_dotenv
from httpx import Headers
from mcp.server.fastmcp import FastMCP

load_dotenv()
mcp = FastMCP("riot")
base_url = "https://americas.api.riotgames.com"


async def make_riot_request(url: str):
    headers = Headers({"X-Riot-Token": os.getenv("RIOT_API_KEY")})  # type: ignore

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

    Returns:
        str: puuid for the given Summoner Name and Tagline
    """
    url = f"{base_url}/riot/account/v1/accounts/by-riot-id/{summoner_name}/{summoner_tagline}"
    response = await make_riot_request(url)

    if response is None:
        return "Error from API"

    return response["puuid"]


@mcp.tool()
async def get_matches_by_summoner(summoner_name: str, summoner_tagline: str) -> dict:
    """Get list of match ids for a summoner name and tagline.

    Args:
        summoner_name: Summoner Name
        summoner_tagline: Summoner Tagline

    Returns:
        dict: Dictionary with a list of match ids.
    """
    puuid = await get_puuid_by_summoner(summoner_name, summoner_tagline)
    url = f"{base_url}/lol/match/v5/matches/by-puuid/{puuid}/ids"
    return await make_riot_request(url)  # type: ignore


@mcp.tool()
async def get_match_details(match_id: str) -> dict:
    """Get all the details available for a given match.

    Args:
        match_id: Match ID that you want details of

    Returns:
        dict: Dictionary with all the details of a given match
    """
    url = f"{base_url}/lol/match/v5/matches/{match_id}"
    return await make_riot_request(url)  # type: ignore


@mcp.tool()
async def get_match_timeline(match_id: str) -> dict:
    """Get the timeline of a given match.

    This gives more details than the `get_match_details` method. Giving detail for each frame of a match.

    Args:
        match_id: Match ID that you want details of

    Returns:
        dict: Dictionary with all the timeline of a given match
    """
    url = f"{base_url}/lol/match/v5/matches/{match_id}/timeline"
    return await make_riot_request(url)  # type: ignore


if __name__ == "__main__":
    mcp.run(transport="stdio")
