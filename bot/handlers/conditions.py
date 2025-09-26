from aiogram import Router, types, F
from bot.buttons.reply import main_menu_keyboard

conditions_router = Router()

@conditions_router.message(F.text == "Shartlar")
async def conditions_handler(message: types.Message):
    conditions_text = "Konkurs shartlari: "
    await message.answer(conditions_text, reply_markup=main_menu_keyboard())