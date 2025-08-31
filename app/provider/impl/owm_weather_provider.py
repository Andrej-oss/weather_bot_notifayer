from typing import Dict

import requests

from app.provider.weather_provider import WeatherProvider

URL = "https://api.openweathermap.org/data/2.5/forecast"


class OWMWeatherProvider(WeatherProvider):

    def __init__(self, api_key: str, lat: float, lon: float):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon

    def fetch(self) -> Dict:
        url = URL
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pl",
        }
        resp = requests.get(url, params=params, timeout=20)
        resp.raise_for_status()
        return resp.json()
