from datetime import datetime, timedelta
from typing import Dict, List, Tuple


class WindAnalyzer:
    def __init__(self, threshold: float, place_name: str, tz):
        self.threshold = threshold
        self.place_name = place_name
        self.tz = tz

    def tomorrow_report(self, js: Dict) -> str:
        tomorrow = (datetime.now(self.tz).date() + timedelta(days=1))
        pairs: List[Tuple[str, float]] = []
        for h in js.get("hourly", []):
            dt = datetime.fromtimestamp(h["dt"], tz=self.tz)
            if dt.date() == tomorrow:
                wind = h.get("wind_speed", 0.0)
                if wind > self.threshold:
                    pairs.append((dt.strftime("%H:%M"), wind))

        if not pairs:
            return (
                f"<b>{self.place_name}</b> — вітер на завтра ({tomorrow}):\n"
                f"Немає годин з швидкістю > {self.threshold:.0f} м/с."
            )

        lines = [f"<b>{self.place_name}</b> — завтра ({tomorrow}), години > {self.threshold:.0f} м/с:"]
        for hhmm, s in pairs:
            lines.append(f"• {hhmm}: {s:.1f} м/с")
        return "\n".join(lines)

    def week_report(self, js: Dict) -> str:
        lines = [f"<b>{self.place_name}</b> — тижневий огляд (макс. вітер за добу):"]
        alert_days = []
        for d in js.get("daily", []):
            dt = datetime.fromtimestamp(d["dt"], tz=self.tz).date()
            wind = d.get("wind_speed", 0.0)
            gust = d.get("wind_gust", 0.0)
            flag = " ✅" if wind > self.threshold else ""
            if flag:
                alert_days.append(str(dt))
            lines.append(f"• {dt}: {wind:.1f} м/с (пориви {gust:.1f}){flag}")

        if alert_days:
            lines.append("")
            lines.append(f"Дні з вітром > {self.threshold:.0f} м/с: {', '.join(alert_days)}")
        else:
            lines.append("")
            lines.append(f"За тиждень поріг > {self.threshold:.0f} м/с не перевищується.")
        return "\n".join(lines)
