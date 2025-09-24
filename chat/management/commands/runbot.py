from django.core.management.base import BaseCommand
from bot import start_bot
import asyncio


class Command(BaseCommand):
    help = "Runs the Telegram bot in polling mode"

    def handle(self, *args, **kwargs):
        async def main():
            bot, dp = await start_bot()
            await dp.start_polling(bot)

        asyncio.run(main())