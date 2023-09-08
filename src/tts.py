import requests
import tempfile
from time import sleep

from config import UBERDUCK_KEY, UBERDUCK_SECRET


def query_uberduck(text, voice="zwf"):
    payload = {
        "voice": voice,
        "pace": 1,
        "speech": text
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
    }

    response = requests.post(
        "https://api.uberduck.ai/speak", json=payload, headers=headers, auth=(UBERDUCK_KEY, UBERDUCK_SECRET))

    audio_uuid = response.json()['uuid']

    for t in range(10):
        sleep(1)
        output = requests.get(
            "https://api.uberduck.ai/speak-status",
            params=dict(uuid=audio_uuid),
            auth=(UBERDUCK_KEY, UBERDUCK_SECRET),
        ).json()

        if output["path"] != None:
            print(output)
            r = requests.get(output["path"], allow_redirects=True)
            tf = tempfile.NamedTemporaryFile(suffix=".wav", mode="wb", delete=False)
            tf.write(r.content)
            tf.close()
            return tf.name
