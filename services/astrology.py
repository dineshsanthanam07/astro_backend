import requests
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ API URLs
CHART_URL = "https://json.astrologyapi.com/v1/horo_chart/D1"
PLANETS_URL = "https://json.astrologyapi.com/v1/planets"

API_KEY = os.getenv("ASTRO_API_KEY")


def call_api(url, payload):
    response = requests.post(
        url,
        headers={
            "Content-Type": "application/json",
            "x-astrologyapi-key": API_KEY
        },
        json=payload
    )

    print("API URL:", url)
    print("Status:", response.status_code)
    print("Response:", response.text)

    if response.status_code != 200:
        raise Exception(response.text)

    return response.json()


def get_chart(payload):

    # ✅ Common payload
    astro_payload = {
        "day": payload["day"],
        "month": payload["month"],
        "year": payload["year"],
        "hour": payload["hour"],
        "min": payload["min"],
        "lat": payload["lat"],
        "lon": payload["lon"],
        "tzone": payload["tzone"]
    }

    # ✅ D1 Chart Structure
    d1_chart = call_api(
        CHART_URL,
        {
            **astro_payload,
            "chartType": "south",
            "image_type": "png"
        }
    )

    # ✅ Planet Details
    planets = call_api(
        PLANETS_URL,
        astro_payload
    )

    # ✅ Final merged response
    final_chart = {
        "lagna_chart": d1_chart,
        "planet_details": planets
    }

    print("FINAL CHART:", final_chart)

    return final_chart