from __future__ import annotations

import requests
import logging
from typing import Dict

from app.data.cache.cache_storage import CacheStorage

URL = "https://api.openweathermap.org/data/2.5/forecast"
logger = logging.getLogger(__name__)


class OWMWeatherProvider:
    def __init__(self, api_key: str, lat: float, lon: float, cache: CacheStorage | None = None):
        self.api_key = api_key
        self.lat = lat
        self.lon = lon
        self.cache = cache

    def fetch(self) -> Dict:
        if self.cache and self.cache.is_valid():
            logger.info("✅ Читаю дані з кешу")
            return self.cache.load()

        logger.info("🌍 Запит до OpenWeather API")
        params = {
            "lat": self.lat,
            "lon": self.lon,
            "appid": self.api_key,
            "units": "metric",
            "lang": "pl",
        }
        resp = requests.get(URL, params=params, timeout=20)
        resp.raise_for_status()
        data = resp.json()

        if self.cache:
            self.cache.save(data)
            logger.info("💾 Дані збережені у кеш")

        return data
