import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import Config
from core.db import AsyncSessionLocal
from core.db_middleware import DbSessionMiddleware
from handlers import command_router, main_router, registration_router

dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=Config.API_TOKEN, parse_mode=ParseMode.HTML)
    dp.update.middleware(
        DbSessionMiddleware(session_pool=AsyncSessionLocal)
    )
    dp.include_routers(
        main_router,
        command_router,
        registration_router,
    )
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
