import logging
from asyncio import sleep

from aiogram import BaseMiddleware
from aiogram.exceptions import TelegramBadRequest, TelegramRetryAfter

logger = logging.getLogger(__name__)
COMMANDS = ['/start', '/menu', '/statistic', '/help']


class ChatClearMiddleware(BaseMiddleware):
    """
    Middleware для удаления кнопок
    предыдущего сообщения при вводе команд.
    """

    def __init__(self):
        super().__init__()

    async def __call__(self, handler, event, data):
        try:
            message = event.message
            if (
                hasattr(message, 'html_text')
                and message.html_text in COMMANDS
            ):
                await message.bot.edit_message_reply_markup(
                    message.chat.id,
                    message.message_id - 1,
                    reply_markup=None,
                )
        except TelegramBadRequest:
            pass
        except TelegramRetryAfter as error:
            await sleep(error.retry_after)
        except Exception as e:
            logger.error(f"Error in command keyboard cleaning: {e}")
        return await handler(event, data)
