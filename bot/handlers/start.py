from aiogram import Router, types
from aiogram.filters import CommandStart
from django.utils import timezone
from asgiref.sync import sync_to_async

router = Router()


@router.message(CommandStart())
async def start_handler(message: types.Message):
    from chat.models import User, Competition
    from bot.buttons.inline import channel_join_keyboard

    user_tg = message.from_user

    @sync_to_async
    def get_or_create_user():
        return User.objects.get_or_create(
            telegram_id=user_tg.id,
            defaults={
                "first_name": user_tg.first_name or "Unknown",
                "last_name": user_tg.last_name,
                "username": user_tg.username,
                "is_premium": user_tg.is_premium or False,
                "created_at": timezone.now(),
            },
        )

    @sync_to_async
    def get_active_competition():
        return Competition.objects.first()

    @sync_to_async
    def get_channels(competition):
        return list(competition.channels.all())

    user, _ = await get_or_create_user()

    competition = await get_active_competition()

    channels = await get_channels(competition)
    if not channels:
        await message.answer("Konkurs uchun kanal yoki guruhlar topilmadi.")
        return

    await message.answer(
        "Konkursda qatnashish uchun quyidagi kanal/guruhlarga a’zo bo’ling:",
        reply_markup=channel_join_keyboard(channels),
    )