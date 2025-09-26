from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def main_menu_keyboard(show_participate: bool = False, is_admin: bool = False) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    buttons = [
        KeyboardButton(text="Konkursda qatnashish") if show_participate else None,
        KeyboardButton(text="Sovg’alar"),
        KeyboardButton(text="Ballarim"),
        KeyboardButton(text="Reyting"),
        KeyboardButton(text="Shartlar"),
    ]
    if is_admin:
        buttons.append(KeyboardButton(text="Admin Paneli"))
    builder.add(*[btn for btn in buttons if btn is not None])
    builder.adjust(1, 2, 2)
    return builder.as_markup(resize_keyboard=True)