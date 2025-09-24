from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text="Konkursda qatnashish"),
        KeyboardButton(text="Sovg’alar"),
        KeyboardButton(text="Ballarim"),
        KeyboardButton(text="Reyting"),
        KeyboardButton(text="Shartlar"),
    ]
    builder.add(*buttons)
    builder.adjust(1, 2, 2)
    return builder.as_markup(resize_keyboard=True)

# async def get_phone_request_keyboard() -> ReplyKeyboardMarkup:
#     builder = ReplyKeyboardBuilder()
#     builder.add(
#         KeyboardButton(text=_("Telefon raqamimni yuborish"), request_contact=True)
#     )
#     return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
#

