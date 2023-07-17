from io import BytesIO
import requests

import time, asyncio

from config import UBERDUCK_KEY, UBERDUCK_SECRET


def query_uberduck(text, voice="zwf"):
    """
    url = "https://api.uberduck.ai/speak"

    payload = {
        "voice": voice,
        "pace": 1,
        "speech": text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    start = time.time()
    response = requests.post(
        url, json=payload, headers=headers, auth=(UBERDUCK_KEY, UBERDUCK_SECRET))

    while True:
        if time.time() - start > 60:
            raise Exception("Request timed out!")
        
        status_url = "https://api.uberduck.ai/speak-status"
        if response.status_code != 200:
            continue

        r = response.json()
        if r['path']:
            return BytesIO(r['path'].read())
            """
    pass


query_uberduck("abcdefg")
