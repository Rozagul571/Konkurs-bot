# bot/handlers/menu.py
from aiogram import Router, types, F
from bot.buttons.reply import main_menu_keyboard
from asgiref.sync import sync_to_async

router = Router()


@router.message(F.text == "Konkursda qatnashish")
async def competition_handler(message: types.Message):
    from chat.models import Competition
    from bot.buttons.inline import channel_join_keyboard

    @sync_to_async
    def get_active_competition():
        return Competition.objects.first()

    @sync_to_async
    def get_channels(competition):
        return list(competition.channels.all())

    competition = await get_active_competition()

    channels = await get_channels(competition)

    await message.answer(
        "Konkursda qatnashish uchun quyidagi kanal/guruhlarga a’zo bo’ling:",
        reply_markup=channel_join_keyboard(channels),
    )


@router.message()
async def default_menu_handler(message: types.Message):
    await message.answer(
        " ",
        reply_markup=main_menu_keyboard(),
    )