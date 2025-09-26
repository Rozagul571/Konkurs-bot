from aiogram import Router, types, F
from asgiref.sync import sync_to_async
from core.models import Prize, Participant
from bot.buttons.reply import main_menu_keyboard

prizes_router = Router()

@prizes_router.message(F.text == "Sovg’alar")
async def prizes_handler(message: types.Message, competition):
    @sync_to_async
    def get_participant(user_id):
        return Participant.objects.filter(user__telegram_id=user_id).first()

    participant = await get_participant(message.from_user.id)
    if not participant:
        await message.answer("Siz hali konkursda qatnashmadingiz.", reply_markup=main_menu_keyboard(show_participate=True))
        return

    prizes = await sync_to_async(list)(Prize.objects.filter(competition=competition).order_by("place"))
    prize_text = (("Konkurs sovg‘alari:\n\n""") + "\n"
                  .join([f"{p.place}-o‘rin: {p.prize_amount}" for p in prizes]))
    await message.answer(prize_text, reply_markup=main_menu_keyboard())