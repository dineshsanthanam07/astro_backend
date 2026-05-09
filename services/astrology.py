import requests
import os
from dotenv import load_dotenv

load_dotenv()  # ADD THIS

API_URL = "https://json.astrologyapi.com/v1/western_horoscope"

def get_chart(payload):
    print("the payload is",payload)
    response = requests.post(
        API_URL,
        headers={
            "x-astrologyapi-key": os.getenv("ASTRO_API_KEY"),
            "Content-Type": "application/json"
        },
        json=payload
    )

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()