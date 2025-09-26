from aiogram import BaseMiddleware
from aiogram.types import Message
import asyncio

class RateLimitMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        await asyncio.sleep(0.1)  # Minimal delay
        return await handler(event, data)