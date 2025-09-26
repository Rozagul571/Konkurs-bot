from aiogram import Router, types, F
from asgiref.sync import sync_to_async
from core.models import Participant
from bot.buttons.reply import main_menu_keyboard

rating_router = Router()

@rating_router.message(F.text == "Reyting")
async def rating_handler(message: types.Message):
    @sync_to_async
    def get_top_participants():
        return list(Participant.objects.order_by('-total_points')[:10])

    participants = await get_top_participants()
    if not participants:
        await message.answer("Hali reytingda hech kim yo‘q.", reply_markup=main_menu_keyboard())
        return

    rating_text = "Top 10 ishtirokchilar:\n" + "\n".join([f"{i+1}. {p.user.full_name or p.user.username} - {p.total_points} ball" for i, p in enumerate(participants)])
    await message.answer(rating_text, reply_markup=main_menu_keyboard())