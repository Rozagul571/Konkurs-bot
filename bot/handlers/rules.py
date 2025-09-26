from aiogram import Router, types, F
from bot.buttons.reply import main_menu_keyboard

terms_router = Router()

@terms_router.message(F.text == "Shartlar")
async def terms_handler(message: types.Message):
    terms_text = (
        "Konkurs shartlari:\n"
        "- Referal orqali +5 ball (Premium uchun +10).\n"
        "- Kanalga qo‘shilish uchun +5 ball (Premium uchun +10).\n"
        "- Tugash sanasi: 2025-10-26.\n"
        "- Natijalar e’lon qilinadi: 2025-10-27."
    )
    await message.answer(terms_text, reply_markup=main_menu_keyboard())