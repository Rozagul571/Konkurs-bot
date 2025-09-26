from aiogram import BaseMiddleware
from aiogram.types import Message
from asgiref.sync import sync_to_async
from core.models import Competition, CompetitionStatus

class CompetitionFilterMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data):
        @sync_to_async
        def get_active_competition():
            return Competition.objects.filter(status=CompetitionStatus.ACTIVE).first()

        competition = await get_active_competition()
        if not competition:
            await event.answer("Hozirda faol konkurs yo‘q.")
            return
        data["competition"] = competition
        return await handler(event, data)