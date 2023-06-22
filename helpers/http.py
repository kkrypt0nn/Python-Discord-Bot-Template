from io import BytesIO
import asyncio
import json
import time

import aiohttp
import os

# Your Uberduck API key and API secret.
# You can create a new key and secret at https://app.uberduck.ai/account/manage
API_KEY = os.environ.get("uberduckapi")
API_SECRET = os.environ.get("uberducksecret")
API_ROOT = "https://api.uberduck.ai"


async def query_uberduck(text, voice="alexa"):
    max_time = 60
    async with aiohttp.ClientSession() as session:
        url = f"{API_ROOT}/speak"
        data = json.dumps(
            {
                "speech": text,
                "voice": voice,
            }
        )

        start = time.time()
        async with session.post(
            url,
            data=data,
            auth=aiohttp.BasicAuth(API_KEY, API_SECRET),
        ) as r:
            if r.status != 200:
                raise Exception("Error synthesizing speech", await r.json())
            uuid = (await r.json())["uuid"]
        while True:
            if time.time() - start > max_time:
                raise Exception("Request timed out!")
            await asyncio.sleep(1)
            status_url = f"{API_ROOT}/speak-status"
            async with session.get(status_url, params={"uuid": uuid}) as r:
                if r.status != 200:
                    continue
                response = await r.json()
                if response["path"]:
                    async with session.get(response["path"]) as r:
                        return BytesIO(await r.read())