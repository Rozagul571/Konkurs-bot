from aiogram import BaseMiddleware
import asyncio


class RateLimitMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        await asyncio.sleep(0.1)
        return await handler(event, data)