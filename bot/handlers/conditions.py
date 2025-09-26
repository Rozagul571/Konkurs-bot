from aiogram import Router, types, F
from asgiref.sync import sync_to_async
from bot.buttons.reply import main_menu_keyboard
from core.models import PointRule, PointAction  # Modelni import qilish

conditions_router = Router()

@sync_to_async
def get_active_rules():
    return list(PointRule.objects.filter(competition__status="active").select_related('competition'))

@conditions_router.message(F.text == "Shartlar")
async def conditions_handler(message: types.Message):
    rules = await get_active_rules()
    if not rules:
        await message.answer("Hozircha hech qanday shartlar belgilanmagan.", reply_markup=main_menu_keyboard())
        return

    conditions_text = "Konkurs shartlari:\n"
    for rule in rules:
        action_text = dict(PointAction.choices)[rule.action_type]
        start_time = rule.start_time.strftime("%Y-%m-%d %H:%M") if rule.start_time else "Belgilanmagan"
        end_time = rule.end_time.strftime("%Y-%m-%d %H:%M") if rule.end_time else "Belgilanmagan"
        conditions_text += ( f"- {action_text}: {rule.points} ball "
            f"(Premium: {rule.multiplier}x, Boshlanish: {start_time}, Tugash: {end_time})\n"
        )

    await message.answer(conditions_text.strip(), reply_markup=main_menu_keyboard())