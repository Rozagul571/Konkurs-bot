from aiogram import Router, types, F
from aiogram.handlers import CallbackQueryHandler
from django.utils import timezone
from asgiref.sync import sync_to_async
import secrets

router = Router()


class MembershipCheckHandler(CallbackQueryHandler):
    async def handle(self) -> None:
        from chat.models import User, Competition, Participant
        from bot.utils.channels import check_channels
        from bot.buttons.reply import main_menu_keyboard
        callback: types.CallbackQuery = self.event
        user_tg = callback.from_user

        @sync_to_async
        def get_active_competition():
            return Competition.objects.first()

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
        def get_or_create_participant(user, competition):
            return Participant.objects.get_or_create(
                user=user,
                competition=competition,
                defaults={
                    "referral_code": secrets.token_urlsafe(8),
                    "total_points": 0,
                    "referrals_count": 0,
                },
            )

        @sync_to_async
        def get_channels(competition):
            return list(competition.channels.all())

        competition = await get_active_competition()

        channels = await get_channels(competition)
        is_missing, not_joined = await check_channels(self.bot, user_tg.id, channels)

        if is_missing:
            await callback.answer(
                f"Siz quyidagi kanal/guruhlarga a’zo emassiz: {', '.join(not_joined)}",
                show_alert=True,)
            return

        user, _ = await get_or_create_user()

        participant, created = await get_or_create_participant(user, competition)

        bot_username = (await self.bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start={participant.referral_code}"
        await callback.message.answer(
            f"Tabriklaymiz! Siz barcha kanal/guruhlarga a’zo bo’ldingiz!\n"
            f"Sizning referal linkingiz: {referral_link}",
            reply_markup=main_menu_keyboard(),
        )
        await callback.answer()


router.callback_query.register(MembershipCheckHandler, F.data == "check_membership")