from aiogram.filters import BaseFilter
from aiogram.types import Message

from core.crud import get_by_id
from core.db import get_async_session
from models import User


class IsEndOnboardingFilter(BaseFilter):
    """
    Фильтр для проверки прохождения онбординга.
    """

    async def __call__(self, message: Message) -> bool:
        session = await get_async_session()

        user = await get_by_id(
            model=User,
            obj_id=message.from_user.id,
            session=session,
        )
        if user:
            await session.close()
            return user.is_onboarding
        await session.close()
        return False
