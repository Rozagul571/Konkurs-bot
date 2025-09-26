from aiogram import Router, types, F
from asgiref.sync import sync_to_async
from aiogram.enums import ParseMode
from core.models import Participant, User, Referral, PointRule, PointAction
from bot.buttons.reply import main_menu_keyboard

referral_router = Router()

@sync_to_async
def get_top_participants():
    participants = Participant.objects.select_related('user').prefetch_related('user__referrals')
    for participant in participants:
        referral_count = participant.user.referrals.count()
        referral_rule = PointRule.objects.filter(
            competition=participant.competition, action_type=PointAction.REFERRAL).first()

        if referral_rule:
            premium_referrals = Referral.objects.filter(referrer=participant.user, referred__is_premium=True).count()
            referral_points = (premium_referrals * referral_rule.points * referral_rule.prem_ball) + ((referral_count - premium_referrals) * referral_rule.points)
            participant.total_points += referral_points
            participant.save()
    return list(participants.order_by('-total_points')[:10])

@referral_router.message(F.text == "Reyting")
async def referral_handler(message: types.Message):
    participants = await get_top_participants()
    if not participants:
        await message.answer("Rating mavjud emas", reply_markup=main_menu_keyboard())
        return

    rating_lines = []
    for i, p in enumerate(participants):
        display_name = p.user.full_name or p.user.username or f"User {i+1}"
        telegram_id = p.user.telegram_id
        link = f"tg://user?id={telegram_id}"
        rating_lines.append(f"{i+1}. [{display_name}]({link}) - {p.total_points} ball")

    rating_text = "Top 10 ishtirokchilar:\n" + "\n".join(rating_lines)
    await message.answer(rating_text, parse_mode=ParseMode.MARKDOWN, reply_markup=main_menu_keyboard())