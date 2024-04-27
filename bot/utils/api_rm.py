import requests
from utils.config import RM_API_TOKEN
import json
URL = "https://api.www.root-me.org/"
AUTEURS = "auteurs/"
CHALLENGE = "challenges/"


def get_user_by_id(id: int):
    url = URL + AUTEURS + str(id)
    cookies = {
        "api_key": RM_API_TOKEN
    }
    headers = {
        "User-Agent" : ""
    }
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        if response.status_code != 200:
            return None
        return_json = json.loads(response.text)
    except Exception:
        return None

    return return_json

def get_all_users_by_name(name: str):
    url = URL + AUTEURS + "?nom=" + name
    cookies = {
        "api_key": RM_API_TOKEN
    }
    headers = {
        "User-Agent" : ""
    }
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        if response.status_code != 200:
            return None
        return_json = json.loads(response.text)[0]
    except Exception:
        return None

    return return_json


def get_challenge_by_id(id: int):
    url = URL + CHALLENGE + str(id)
    cookies = {
        "api_key": RM_API_TOKEN
    }
    headers = {
        "User-Agent" : ""
    }
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        if response.status_code != 200:
            return None
        return_json = json.loads(response.text)[0]
    except Exception:
        return None

    return return_json


def get_all_chall_by_name(name: str):
    url = URL + CHALLENGE + "?titre=" + name
    cookies = {
        "api_key": RM_API_TOKEN
    }
    headers = {
        "User-Agent" : ""
    }
    try:
        response = requests.get(url, cookies=cookies, headers=headers)
        if response.status_code != 200:
            return None
        return_json = json.loads(response.text)[0]
    except Exception:
        return None

    return return_json
