import os
import json
from datetime import datetime, timedelta
from typing import Dict


class CacheStorage:
    def __init__(self, cache_file: str, ttl: timedelta):
        self.cache_file = cache_file
        self.ttl = ttl

    def is_valid(self) -> bool:
        if not os.path.exists(self.cache_file):
            return False
        try:
            with open(self.cache_file, "r", encoding="utf-8") as f:
                cache = json.load(f)
            ts = datetime.fromisoformat(cache["timestamp"])
            return datetime.utcnow() - ts < self.ttl
        except Exception:
            return False

    def load(self) -> Dict:
        with open(self.cache_file, "r", encoding="utf-8") as f:
            cache = json.load(f)
        return cache["data"]

    def save(self, data: Dict):
        cache = {"timestamp": datetime.utcnow().isoformat(), "data": data}
        with open(self.cache_file, "w", encoding="utf-8") as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
