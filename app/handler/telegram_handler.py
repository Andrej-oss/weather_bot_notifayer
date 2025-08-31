from telegram import Update
from telegram.ext import ContextTypes

from app.service.notifier.impl.telegram_notifier import TelegramNotifier
from app.provider.impl.owm_weather_provider import OWMWeatherProvider
from app.service.analizer.wind_analyzer import WindAnalyzer


class TelegramHandlers:
    def __init__(self, storage, place_name, lat, lon, api_key, threshold, tz):
        self.storage = storage
        self.place_name = place_name
        self.lat, self.lon = lat, lon
        self.api_key = api_key
        self.threshold = threshold
        self.tz = tz

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
        chat_id = update.effective_chat.id
        provider = OWMWeatherProvider(self.api_key, self.lat, self.lon)
        analyzer = WindAnalyzer(self.threshold, self.place_name, self.tz)
        notifier = TelegramNotifier(context.application)
        js = provider.fetch()
        await notifier.send(chat_id, analyzer.tomorrow_report(js))
        await notifier.send(chat_id, analyzer.week_report(js))
