from aiogram import Dispatcher
from .middlewares import RateLimitMiddleware
from .handlers import start_router, callback_router, menu_router


def register_handlers(dp: Dispatcher) -> None:
    dp.message.middleware(RateLimitMiddleware())
    dp.include_router(start_router)
    dp.include_router(callback_router)
    dp.include_router(menu_router)

