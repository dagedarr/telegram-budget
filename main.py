# ----------------------- telegram pooling ver -----------------------

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



# ----------------------- telegram webhook ver for pythonanywhere -----------------------

# import asyncio
# import logging
# import sys

# from aiogram import Bot, Dispatcher, types
# from aiogram.client.session.aiohttp import AiohttpSession
# from aiogram.enums import ParseMode
# from flask import Flask, request
# from flask_sslify import SSLify

# from config import Config
# from core.db import AsyncSessionLocal
# from core.db_middleware import DbSessionMiddleware
# from handlers import handlers_router
# from utils.middlewares import ChatClearMiddleware


# dp = Dispatcher()

# session = AiohttpSession(proxy="http://proxy.server:3128")
# bot = Bot(
#     token=Config.API_TOKEN,
#     parse_mode=ParseMode.HTML,
#     session=session
# )

# dp.update.middleware(ChatClearMiddleware())
# dp.update.middleware(
#     DbSessionMiddleware(session_pool=AsyncSessionLocal)
# )
# dp.include_routers(handlers_router)

# app = Flask(__name__)
# sslify = SSLify(app)


# @app.route('/', methods=["POST", "GET"])
# def bot_webhook():
#     if request.method == 'POST':

#         response = request.get_json()
#         telegram_update = types.Update(**response)

#         # just for pythonanywhere free plan
#         # else dp.feed_update(bot=bot, update=telegram_update)
#         loop = asyncio.get_event_loop()
#         loop.run_until_complete(dp.feed_update(bot=bot, update=telegram_update))

#         return 'OK', 200
#     return 'Hello world!'


# if __name__ == "__main__":
#     logging.basicConfig(level=logging.INFO, stream=sys.stdout)

#     app.run(threaded=True)

# # pip3 install flask flask-sslify aiohttp-socks

# # you need to set webhook begore using:
# # https://api.telegram.org/bot{BOT_TOKEN}/setWebhook?url={YOUR_PYTHONANYWHERE_URL}