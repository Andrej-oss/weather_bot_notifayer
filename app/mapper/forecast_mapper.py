from datetime import datetime
from typing import Dict, List

from app.model.forecast_dto import ForecastDto


class OWMForecastMapper:

    @staticmethod
    def map_list(data: Dict) -> List[ForecastDto]:
        return [OWMForecastMapper.map_item(item) for item in data.get("list", [])]

    @staticmethod
    def map_item(item: Dict) -> ForecastDto:
        return ForecastDto(
            time=OWMForecastMapper._format_time(item["dt"]),
            temp=round(item["main"]["temp"], 1),
            feels_like=round(item["main"]["feels_like"], 1),
            description=item["weather"][0]["description"],
            wind_speed=item["wind"]["speed"],
            humidity=item["main"]["humidity"],
            rain=item.get("rain", {}).get("3h", 0.0),
            icon=item["weather"][0]["icon"],
        )

    # --- приватні ---
    @staticmethod
    def _format_time(timestamp: int) -> str:
        return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M")