import asyncio, os
from telegram.ext import Application, CommandHandler
import pytz
from dotenv import load_dotenv
import nest_asyncio

from app.data.subscribers_storage import SubscribersStorage
from app.handler.telegram_handler import TelegramHandlers
from app.service.scheduler.telegram_scheduler import Scheduler

load_dotenv()

PLACE_NAME = "Chałupy, PL"
LAT, LON = 54.741, 18.541
TIMEZONE = pytz.timezone("Europe/Warsaw")
SUBSCRIBERS_DB = "subscribers.json"
WIND_THRESHOLD_MS = float(os.environ.get("WIND_THRESHOLD_MS", 5.0))
SEND_HOUR_LOCAL = int(os.environ.get("SEND_HOUR_LOCAL", 20))
OWM_API_KEY = os.environ["OWM_API_KEY"]


async def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit("TELEGRAM_BOT_TOKEN не встановлено")

    app = Application.builder().token(token).build()

    storage = SubscribersStorage(SUBSCRIBERS_DB)
    handlers = TelegramHandlers(storage, PLACE_NAME, LAT, LON, OWM_API_KEY, WIND_THRESHOLD_MS, TIMEZONE)

    app.add_handler(CommandHandler("start", handlers.start))
    app.add_handler(CommandHandler("stop", handlers.stop))
    app.add_handler(CommandHandler("now", handlers.now))

    scheduler = Scheduler(app, None, TIMEZONE, SEND_HOUR_LOCAL)
    # тут можна під'єднати scheduled_job так само як now

    print("Бот запущений.")
    await app.run_polling(close_loop=False)

if __name__ == "__main__":
    nest_asyncio.apply()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except (KeyboardInterrupt, SystemExit):
        print("Зупинено.")

