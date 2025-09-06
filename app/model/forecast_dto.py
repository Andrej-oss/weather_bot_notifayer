from dataclasses import dataclass


@dataclass
class ForecastDto:
    time: str
    temp: float
    feels_like: float
    description: str
    wind_speed: float
    humidity: int
    rain: float
    icon: str