from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def channel_join_keyboard(channels) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for channel in channels:
        text = channel.title or channel.channel_username
        url = f"https://t.me/{channel.channel_username.lstrip('@')}"
        builder.button(text=text, url=url)
    builder.button(text="A'zo bo'ldim", callback_data="check_membership")
    builder.adjust(1)
    return builder.as_markup()