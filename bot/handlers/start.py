from aiogram import Router, types, F
from aiogram.types import Message
from core.models import User, Competition, Participant, CompetitionStatus
from bot.utils.check_channels import check_user_channels
from asgiref.sync import sync_to_async
from django.db import transaction
from bot.buttons.inline import channel_join_keyboard
from bot.buttons.reply import main_menu_keyboard
import uuid
from django.utils import timezone

start_router = Router()

@sync_to_async
def get_or_create_user(telegram_id, username, full_name, is_premium):
    return User.objects.get_or_create(
        telegram_id=telegram_id,
        defaults={
            "username": username,
            "full_name": full_name,
            "is_premium": is_premium,
            "role": "premium" if is_premium else "participant",
            "joined_at": timezone.now(),
            "referral_code": str(uuid.uuid4())[:50],
        }
    )[0]

@sync_to_async
def get_or_create_participant(user, competition):
    with transaction.atomic():
        participant, created = Participant.objects.get_or_create(
            user=user,
            competition=competition,
            defaults={'is_active': False, 'total_points': 0}
        )
        return participant, created

@start_router.message(F.text == "/start")
async def start_handler(message: Message, competition):
    telegram_id = message.from_user.id
    username = message.from_user.username
    full_name = message.from_user.full_name or f"{message.from_user.first_name} {message.from_user.last_name or ''}".strip()
    is_premium = message.from_user.is_premium or False

    user = await get_or_create_user(telegram_id, username, full_name, is_premium)
    participant, _ = await get_or_create_participant(user, competition)

    channels = await sync_to_async(list)(competition.channels.all())
    if channels:
        is_member, not_joined = await check_user_channels(message.bot, telegram_id, [ch.channel_username for ch in channels])
        if not is_member:
            not_joined_channels = [ch for ch in channels if ch.channel_username in not_joined]
            await message.answer(
                "Iltimos, quyidagi kanallarga/guruhlarga a'zo bo'ling va 'A’zo bo‘ldim' tugmasini bosing:",
                reply_markup=channel_join_keyboard(not_joined_channels)
            )
            return

    bot_username = (await message.bot.get_me()).username
    referral_link = f"https://t.me/{bot_username}?start={user.referral_code}"
    await message.answer(
        f"Tabriklaymiz! Siz barcha kanal/guruhlarga a’zo bo‘ldingiz!\n"
        f"Sizning referal linkingiz: {referral_link}",
        reply_markup=main_menu_keyboard(show_participate=False, is_admin=user.role == "admin")
    )