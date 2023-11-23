from datetime import datetime
from re import findall, match, search
from typing import Optional, Tuple, Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import create, get_by_attributes
from models import Alias, Category, Transaction

from .user_actions import callback_message


class TransactionCallbackData(CallbackData, prefix='transaction'):
    trans_id: int


async def parse_text_for_amount_and_category(
    text: str
) -> Tuple[Optional[Union[float, int]], Optional[str]]:
    """
    Функция для вычленения суммы и категории из сообщения пользователя.

    Args:
        text (str): Текст сообщения.

    Возвращает кортеж с извлеченными данными. Первый элемент -
    сумма (если найдена), второй элемент - категория (если найдена).
    """

    # Ищем сумму в тексте
    amount_match = search(r'(\d+(?:,\d+)?(?:\.\d+)?)', text)
    amount = float(amount_match.group().replace(
        ',', '.')) if amount_match else None

    # Ищем категорию в тексте
    words = findall(r'\b\w+\b', text)
    numbers = [word for word in words if not match(r'\d+(\.\d+)?', word)]
    category_title = ' '.join(numbers) if numbers else None

    return amount, category_title


async def amount_validate(
    amount: Optional[Union[int, float]], message: Message
) -> Optional[Union[int, float]]:
    """
    Проверяет сумму на валидность.

    Args:
        amount (Optional[Union[int, float]]): Сумма транзакции.
        message (Message): Объект сообщения.

    Returns:
        Optional[Union[int, float]]: Валидная сумма транзакции или None,
        если сумма не валидна.
    """

    if not amount:
        await callback_message(
            target=message,
            text='Я не смог распознать сумму транзакции, попробуй еще раз!',
            delete_reply=False
        )
    return amount


async def get_category_or_alias_id(
    title: Optional[str], message: Message, session: AsyncSession
) -> Tuple[Optional[int], Optional[int]]:
    """
    Получает id категории и алиаса по заданному заголовку.

    Args:
        title (Optional[str]): Заголовок категории или алиаса.
        message (Message): Объект сообщения.
        session (AsyncSession): Сессия SQLAlchemy.

    Returns:
        Optional[Tuple[Optional[int], Optional[int]]]: Кортеж с id категории
        и алиаса(если найдены).
    """

    category: Optional[Category] = await get_by_attributes(
        model=Category,
        attributes={
            'user_id': message.from_user.id,
            'title': title
        },
        session=session
    )
    if category:
        alias: Optional[Alias] = await get_by_attributes(
            model=Alias,
            attributes={
                'user_id': message.from_user.id,
                'category_id': category.id,
                'title': title
            },
            session=session
        )
        return category.id, alias.id if alias else None

    alias: Optional[Alias] = await get_by_attributes(
        model=Alias,
        attributes={
            'user_id': message.from_user.id,
            'title': title
        },
        session=session
    )
    if alias:
        return alias.category_id, alias.id


async def create_transaction(
    session: AsyncSession,
    user_id: int,
    category_id: int,
    alias_id: Optional[int],
    amount: float
) -> Transaction:
    """
    Создает транзакцию в БД и возвращает ее.

    Args:
        session (AsyncSession): Сессия SQLAlchemy.
        user_id (int): ID пользователя.
        category_id (int): ID категории.
        alias_id (Optional[int]): ID алиаса (если есть).
        amount (float): Сумма транзакции.

    Returns:
        Transaction: Созданная транзакция.
    """

    transaction = await create(
        session=session,
        model=Transaction,
        user_id=user_id,
        date=datetime.now().timestamp(),
        category_id=category_id,
        alias_id=alias_id if alias_id else None,
        amount=amount
    )
    return transaction


async def get_transactions_message(transactions):
    """
    Генерирует текстовое сообщение на основе списка объектов Transaction.

    Args:
        transactions (List[Transaction]): Список объектов Transaction.

    Returns:
        str: Текстовое сообщение с информацией о транзакциях.
    """

    message = ('Список последних трат. Для удаление нажмите ' +
               'на /del_tr справа от траты\n\n')

    # Создаем список строк для каждой транзакции
    transaction_strings = [
        f'{trans}; /del_tr{trans.id}' for trans in transactions
    ]

    # Объединяем строки в одну
    message += '\n'.join(transaction_strings)

    return message


async def validate_transaction_for_del(
    transaction_id_from_msg: int,
    transaction: Transaction,
    user_id: int,
) -> Optional[str]:

    if not transaction_id_from_msg:
        return 'Выберите транзакцию для удаления!\nНапример, /del_tr198'

    if not transaction or user_id != transaction.user_id:
        return 'Это не Ваша транзакция!'
