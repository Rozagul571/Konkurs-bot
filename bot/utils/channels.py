# bot/utils/channels.py
from aiogram import Bot
from aiogram.methods import GetChatMember
from aiogram.exceptions import TelegramAPIError
from typing import List, Tuple
from chat.models import Channel


async def check_channels(bot: Bot, user_id: int, channels: List[Channel]) -> Tuple[bool, List[str]]:
    not_joined = []
    for channel in channels:
        try:
            result = await bot(
                GetChatMember(chat_id=channel.channel_username, user_id=user_id ))

            if result.status in ("left", "kicked"):
                not_joined.append(channel.channel_username)
        except TelegramAPIError as e:
            not_joined.append(channel.channel_username)
            print(f"Error checking {channel.channel_username}: {e}")
    return bool(not_joined), not_joined