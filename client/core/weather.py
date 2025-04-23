from typing import Any
import requests
from utils.globals import url

def get_weather(city) -> (bool, dict[str,Any]):
    res = requests.get(f"{url}/weather/{city}")
    if res.status_code == 200:
        return True,res.json()
    return False,None

def get_weather_by_coords(lat, lon) -> (bool, dict[str,Any]):
    try:
        response = requests.get(f"{url}/weather/coords", params={
            "lat": lat,
            "lon": lon
        })
        response.raise_for_status()
        return True,response.json()
    except requests.exceptions.RequestException as e:
        return False,None