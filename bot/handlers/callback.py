from aiogram import Router, types, F, Bot
from aiogram.handlers import CallbackQueryHandler
from django.utils import timezone
from asgiref.sync import sync_to_async
import uuid
from core.models import User, Competition, Participant, Point, PointRule, PointAction, Referral
from bot.buttons.inline import channel_join_keyboard
from bot.buttons.reply import main_menu_keyboard
from bot.utils.check_channels import check_user_channels

callback_router = Router()

class MembershipCheckHandler(CallbackQueryHandler):
    async def handle(self) -> None:
        callback: types.CallbackQuery = self.event
        user_tg = callback.from_user
        bot: Bot = self.bot

        @sync_to_async
        def get_or_create_user():
            return User.objects.get_or_create(telegram_id=user_tg.id,
                defaults={
                    "full_name": (user_tg.first_name or "") + " " + (user_tg.last_name or ""),
                    "username": user_tg.username,
                    "is_premium": user_tg.is_premium or False,
                    "role": "premium" if user_tg.is_premium else "participant",
                    "referral_code": str(uuid.uuid4())[:50],
                    "joined_at": timezone.now(),
                },
            )[0]

        @sync_to_async
        def get_active_competition():
            return Competition.objects.filter(status__in=["active", "pending"]).first()

        @sync_to_async
        def get_or_create_participant(user, competition):
            return Participant.objects.get_or_create(
                user=user,
                competition=competition,
                defaults={"is_active": False, "total_points": 0})[0]

        @sync_to_async
        def get_channels(competition):
            return list(competition.channels.all())

        @sync_to_async
        def award_channel_join_points(participant):
            rule = PointRule.objects.filter(
                competition=participant.competition, action_type=PointAction.CHANNEL_JOIN
            ).first()
            if rule and not Point.objects.filter(
                participant=participant, reason=PointAction.CHANNEL_JOIN
            ).exists():
                points = rule.points * (2 if participant.user.is_premium else 1)
                Point.objects.create(participant=participant, points=points, reason=PointAction.CHANNEL_JOIN)
                participant.total_points += points
                participant.save()

        @sync_to_async
        def count_referrals(user):
            return Referral.objects.filter(referrer=user).count()

        user = await get_or_create_user()
        competition = await get_active_competition()


        participant = await get_or_create_participant(user, competition)
        channels = await get_channels(competition)
        is_member, not_joined = await check_user_channels(bot, user_tg.id, [ch.channel_username for ch in channels])

        bot_username = (await bot.get_me()).username
        referral_link = f"https://t.me/{bot_username}?start={user.referral_code}"

        if not is_member:
            await callback.answer(
                f"Siz quyidagi kanal/guruhlarga a’zo emassiz: {', '.join(not_joined)}",
                show_alert=True)

            await callback.message.edit_reply_markup(reply_markup=channel_join_keyboard([ch for ch in channels if ch.channel_username in not_joined]))
        else:

            participant.is_active = True
            await sync_to_async(participant.save)()
            await award_channel_join_points(participant)
            referral_count = await count_referrals(user)
            referral_rule = await sync_to_async(PointRule.objects.filter)(
                competition=competition, action_type=PointAction.REFERRAL).first()


            if referral_rule:
                referral_points = referral_count * referral_rule.points * (2 if user.is_premium else 1)
                if referral_points > 0 and not Point.objects.filter(
                    participant=participant, reason=PointAction.REFERRAL
                ).exists():
                    Point.objects.create(participant=participant, points=referral_points, reason=PointAction.REFERRAL)
                    participant.total_points += referral_points
                    await sync_to_async(participant.save)()

            await callback.message.answer(
                f"Tabriklaymiz.  Siz barcha kanal/guruhlarga a’zo bo‘ldingiz!\n"
                
                f"Sizning referal linkingiz: {referral_link}\n"
                f"Jami ballar: {participant.total_points}",
                reply_markup=main_menu_keyboard(show_participate=False, is_admin=user.role == "admin")
            )
            await callback.message.delete()
            await callback.answer()

callback_router.callback_query.register(MembershipCheckHandler, F.data == "check_membership")