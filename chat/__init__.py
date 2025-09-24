from aiogram import Bot, Dispatcher
from django.conf import settings

from bot import register_handlers


async def start_bot():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    register_handlers(dp)
    return bot, dp