from telegram import Update
from telegram.ext import ContextTypes

from app.service.notifier.impl.telegram_notifier import TelegramNotifier
from app.provider.impl.owm_weather_provider import OWMWeatherProvider
from app.service.analizer.wind_analyzer import WindAnalyzer
from app.service.weather_service import WeatherService


class TelegramHandlers:
    def __init__(self, storage, place_name, lat, lon, api_key, threshold, tz, cache):
        self.storage = storage
        self.place_name = place_name
        self.lat, self.lon = lat, lon
        self.api_key = api_key
        self.threshold = threshold
        self.tz = tz
        self.cache = cache

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        subs = set(self.storage.load())
        subs.add(chat_id)
        self.storage.save(sorted(list(subs)))
        await update.message.reply_text(
            "Підписка активована! Щодня о 20:00 надсилатиму:\n"
            "— Завтра по годинах\n"
            "— Тижневий огляд\n\n"
            f"Локація: {self.place_name}, поріг: {self.threshold:.0f} м/с"
        )

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        chat_id = update.effective_chat.id
        subs = set(self.storage.load())
        if chat_id in subs:
            subs.remove(chat_id)
            self.storage.save(sorted(list(subs)))
            await update.message.reply_text("Відписка успішна.")
        else:
            await update.message.reply_text("Ви не були підписані.")

    async def now(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Відправляє звіт лише поточному користувачу (/now)."""
        chat_id = update.effective_chat.id
        await self._send_reports([chat_id], context.application)

    async def scheduled_job(self, app):
        """Відправляє звіт усім підписникам (через Scheduler)."""
        subscribers = self.storage.load()
        if not subscribers:
            print("Немає підписників для розсилки.")
            return
        await self._send_reports(subscribers, app)

    async def _send_reports(self, chat_ids, app):
        provider = OWMWeatherProvider(self.api_key, self.lat, self.lon)
        service = WeatherService(provider)  # ✅ замість analyzer

        notifier = TelegramNotifier(app)

        message = service.get_forecast_with_strong_wind()

        for chat_id in chat_ids:
            try:
                await notifier.send(chat_id, message)
            except Exception as e:
                print(f"Не вдалося надіслати {chat_id}: {e}")
