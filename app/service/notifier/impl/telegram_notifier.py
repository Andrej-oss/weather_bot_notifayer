from telegram.constants import ParseMode

from app.service.notifier.notifier import Notifier


class TelegramNotifier(Notifier):
    def __init__(self, app):
        self.app = app

    async def send(self, chat_id: str, message: str):
        await self.app.bot.send_message(
            chat_id, message, parse_mode=ParseMode.HTML, disable_web_page_preview=True
        )
