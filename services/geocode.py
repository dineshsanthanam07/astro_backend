import requests
import os
from dotenv import load_dotenv

load_dotenv()  # ADD THIS

def get_lat_lon(city: str):
    url = f"https://api.opencagedata.com/geocode/v1/json?q={city}&key={os.getenv('GEOCODE_API_KEY')}"
    
    res = requests.get(url).json()

    if not res["results"]:
        raise Exception("City not found")

    lat = res["results"][0]["geometry"]["lat"]
    lon = res["results"][0]["geometry"]["lng"]
    print("the lon and lat is",lat,lon)
    return lat, lon