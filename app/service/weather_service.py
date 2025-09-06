from app.mapper.forecast_mapper import OWMForecastMapper
from app.provider.impl.owm_weather_provider import OWMWeatherProvider


class WeatherService:
    def __init__(self, provider: OWMWeatherProvider):
        self.provider = provider

    def get_forecast_with_strong_wind(self) -> str:
        raw = self.provider.fetch()
        forecasts = OWMForecastMapper.map_list(raw)

        strong_wind = [f for f in forecasts if f.wind_speed > 5]

        if not strong_wind:
            return "🌤 Вітру більше 5 м/с у прогнозі не очікується."

        lines = ["🌬 Прогноз з сильним вітром (>5 м/с):\n"]
        for f in strong_wind:
            icon = self._map_icon(f.icon)
            lines.append(
                f"{f.time} {icon} {f.description.capitalize()}, "
                f"🌡 {f.temp}°C (відчувається {f.feels_like}°C), "
                f"💨 {f.wind_speed} м/с, 💧 {f.humidity}%, "
                f"☔ {f.rain} мм"
            )

        return "\n".join(lines)

    @staticmethod
    def _map_icon(code: str) -> str:
        """Перетворює іконку OWM на емодзі."""
        mapping = {
            "01d": "☀️", "01n": "🌙",
            "02d": "🌤", "02n": "☁️🌙",
            "03d": "☁️", "03n": "☁️",
            "04d": "☁️", "04n": "☁️",
            "09d": "🌧", "09n": "🌧",
            "10d": "🌦", "10n": "🌧",
            "11d": "🌩", "11n": "🌩",
            "13d": "❄️", "13n": "❄️",
            "50d": "🌫", "50n": "🌫",
        }
        return mapping.get(code, "❔")