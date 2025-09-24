# bot/__init__.py
import django
from aiogram import Bot, Dispatcher
from django.conf import settings
from .distpatchers import register_handlers


async def start_bot():
    django.setup()
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    register_handlers(dp)
    return bot, dp