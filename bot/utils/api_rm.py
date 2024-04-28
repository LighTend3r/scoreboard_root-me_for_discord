import aiohttp
import json
from utils.config import RM_API_TOKEN

URL = "https://api.www.root-me.org/"
AUTEURS = "auteurs/"
CHALLENGE = "challenges/"

async def get_user_by_id(id: int):
    url = URL + AUTEURS + str(id)
    headers = {"User-Agent": ""}
    cookies = {"api_key": RM_API_TOKEN}
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                return_json = await response.json()
        except Exception:
            return None
    return return_json

async def get_all_users_by_name(name: str):
    url = URL + AUTEURS + "?nom=" + name
    headers = {"User-Agent": ""}
    cookies = {"api_key": RM_API_TOKEN}
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                return_json = (await response.json())[0]
        except Exception:
            return None
    return return_json

async def get_challenge_by_id(id: int):
    url = URL + CHALLENGE + str(id)
    headers = {"User-Agent": ""}
    cookies = {"api_key": RM_API_TOKEN}
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                return_json = (await response.json())[0]
        except Exception:
            return None
    return return_json

async def get_all_chall_by_name(name: str):
    url = URL + CHALLENGE + "?titre=" + name
    headers = {"User-Agent": ""}
    cookies = {"api_key": RM_API_TOKEN}
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        try:
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                return_json = (await response.json())[0]
        except Exception:
            return None
    return return_json
