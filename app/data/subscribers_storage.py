import json, os
from typing import List


class SubscribersStorage:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def load(self) -> List[int]:
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                return list({int(x) for x in json.load(f)})
        except Exception:
            return []

    def save(self, chat_ids: List[int]):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(sorted(list({int(x) for x in chat_ids})), f, ensure_ascii=False, indent=2)
