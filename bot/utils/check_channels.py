from aiogram import Bot
from aiogram.types import User
import asyncio

from config.settings import TELEGRAM_BOT_TOKEN
bot = Bot(token=TELEGRAM_BOT_TOKEN)

async def check_user_channels(bot: Bot, user_id: int, channel_usernames: list[str]) -> tuple[bool, list]:
    """
    Foydalanuvchi berilgan kanallarga a'zo ekanligini tekshiradi.
    Qaytaradi: (barcha a'zo bo'lganligi, a'zo bo'lmagan kanallar ro'yxati)
    """
    not_joined = []
    for channel in channel_usernames:
        try:
            member = await bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                not_joined.append(channel)
        except Exception as e:
            print(f"Xatolik {channel} uchun: {e}")
            not_joined.append(channel)
    return len(not_joined) == 0, not_joined