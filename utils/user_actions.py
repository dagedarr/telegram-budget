from typing import Union

from aiogram.types import CallbackQuery, Message
from aiogram.utils.keyboard import InlineKeyboardMarkup
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_by_id
from models import User


async def make_onboarding_end(
    user_id: int,
    session: AsyncSession,
    default_username: str
):
    user = await get_by_id(
        model=User,
        obj_id=user_id,
        session=session
    )
    if not user.username:
        user.username = default_username
    user.is_onboarding = True
    await session.commit()


async def callback_message(
    target: Union[Message, CallbackQuery],
    text: str,
    reply_markup: InlineKeyboardMarkup = None,
    replace_message: bool = False,
    **kwargs,
):
    """Редактировние сообщения."""
    target = target if isinstance(target, Message) else target.message

    if replace_message:
        await target.edit_text(
            text=text,
            reply_markup=reply_markup,
            **kwargs
        )
    else:
        await target.answer(
            text=text,
            reply_markup=reply_markup,
            **kwargs
        )
        await target.delete_reply_markup()
