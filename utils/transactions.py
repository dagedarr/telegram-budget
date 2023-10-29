from re import search
from typing import Tuple

from core.crud import create
from sqlalchemy.ext.asyncio import AsyncSession
from models import Transaction
from datetime import datetime


class EmptyTextError(Exception):
    """Исключение для парсера, вызывается если нам передан пустое сообщение"""
    pass


async def parse_text_for_amount_and_category(
    text: str
) -> Tuple[float, str]:
    # if not text:
    #     raise EmptyTextError
    if text == "1":
        raise EmptyTextError
    amount_match = search(r'\d+', text)
    amount = float(amount_match.group()) if amount_match else None

    category_match = search(r'\D+', text)
    category_title = str(
        category_match.group().strip()
    ) if category_match else None

    return amount, category_title


async def create_transaction(
    session: AsyncSession,
    user_id: int,
    category_id: int,
    amount: float
) -> Tuple[float, int]:
    """
    Создает транзакцию в БД и возвращает пользователю сумму и id категории.
    """
    await create(
        session=session,
        model=Transaction,
        user_id=user_id,
        date=datetime.now().timestamp(),
        category_id=category_id,
        amount=amount
    )

    return amount, category_id
