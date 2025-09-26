from aiogram import Router, types, F
from asgiref.sync import sync_to_async
from core.models import Participant, User
from bot.buttons.reply import main_menu_keyboard

user_router = Router()

@user_router.message(F.text == "Ballarim")
async def points_handler(message: types.Message):
    @sync_to_async
    def get_participant(user_id):
        return Participant.objects.filter(user__telegram_id=user_id).first()

    participant = await get_participant(message.from_user.id)
    if not participant:
        await message.answer("Siz hali konkursda qatnashmadingiz.", reply_markup=main_menu_keyboard(show_participate=True))
        return

    await message.answer(f"Sizning jami ballaringiz: {participant.total_points}", reply_markup=main_menu_keyboard())