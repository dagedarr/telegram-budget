import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import Config
from core.db import AsyncSessionLocal
from core.db_middleware import DbSessionMiddleware
from handlers import handlers_router
from utils.middlewares import ChatClearMiddleware

dp = Dispatcher()


async def main() -> None:
    bot = Bot(token=Config.API_TOKEN, parse_mode=ParseMode.HTML)
    dp.update.middleware(ChatClearMiddleware())
    dp.update.middleware(
        DbSessionMiddleware(session_pool=AsyncSessionLocal)
    )
    dp.include_routers(handlers_router)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())


# celery -A tasks.tasks:app worker --loglevel=INFO --pool=solo
# celery -A tasks.tasks:app flower
