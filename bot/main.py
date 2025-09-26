import os
import asyncio

# Django sozlamalarini yuklash
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
import django
django.setup()

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.middlewares import RateLimitMiddleware, CompetitionFilterMiddleware
from config.settings import TELEGRAM_BOT_TOKEN

# Handlersni faqat funksiya ichida import qilish
async def setup_routers(dp):
    from bot.handlers.start import start_router
    from bot.handlers.user import user_router
    from bot.handlers.referral import referral_router
    from bot.handlers.prizes import prizes_router
    from bot.handlers.conditions import conditions_router
    dp.include_router(start_router)
    dp.include_router(user_router)
    dp.include_router(referral_router)
    dp.include_router(prizes_router)
    dp.include_router(conditions_router)

async def main():
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())

    # Middlewares
    dp.message.middleware(RateLimitMiddleware())
    dp.message.middleware(CompetitionFilterMiddleware())

    # Routersni o'rnatish
    await setup_routers(dp)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())