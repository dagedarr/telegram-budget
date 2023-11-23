from datetime import datetime, timedelta
from enum import Enum, StrEnum

from aiogram.filters.callback_data import CallbackData
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from core.crud import get_by_id
from models import User


class TimeInterval(StrEnum):
    MONTH = 'month'
    YEAR = 'year'
    TOTAL = 'total'


class OutputMode(Enum):
    TG_CHAT = {
        'TAG': '\n',
        'BOLD_TAG_START': '<b>',
        'BOLD_TAG_END': '</b>'
    }
    MAIL = {
        'TAG': '<br>',
        'BOLD_TAG_START': '<b>',
        'BOLD_TAG_END': '</b>'
    }
    GOOGLE_SHEETS = {
        'TAG': '',
        'BOLD_TAG_START': '',
        'BOLD_TAG_END': ''
    }


class StatisticCallbackData(CallbackData, prefix='statistic'):
    action: str
    time_interval: str


async def set_statistic_msg(
    user_id: int,
    time_interval: TimeInterval,
    session: AsyncSession,
    output_mode: OutputMode
) -> str:
    """
    Создает текст сообщения пользователю с его тратами по
    Категориям и Алиасам за выбранный промежуток времени.

    Parameters:
    - user_id (int): Идентификатор пользователя.
    - time_interval (TimeInterval): Выбранный временной интервал.
    - session (AsyncSession): Асинхронная сессия для взаимодействия с БД.
    - output_mode (OutputMode): Режим работы функции.

    Returns:
        str: Сформированное сообщение со статистикой расходов пользователя.
    """

    TAG = output_mode.value['TAG']
    BOLD_TAG_START = output_mode.value['BOLD_TAG_START']
    BOLD_TAG_END = output_mode.value['BOLD_TAG_END']

    user = await get_by_id(model=User, obj_id=user_id, session=session)

    start_time, label = get_interval_label(
        time_interval=time_interval
    )

    result = [
        f'{BOLD_TAG_START}Сводка Расходов в период {label}{BOLD_TAG_END}{TAG}'
    ]

    total_expense = 0

    for category in user.categories:
        category_expense = sum(
            transaction.amount for transaction in category.transactions
            if datetime.fromtimestamp(transaction.date) >= start_time
        )

        total_expense += category_expense

        if category_expense > 0:
            text = (f'{BOLD_TAG_START}{category.title}: '
                    f'{category_expense} ₽{BOLD_TAG_END}')
            result.append(text)

        all_aliases_expense = 0

        for alias in category.aliases:
            alias_expense = sum(
                transaction.amount for transaction in alias.transactions
                if datetime.fromtimestamp(transaction.date) >= start_time
            )

            all_aliases_expense += alias_expense
            if alias_expense > 0:
                result.append(f'--{alias.title}: {alias_expense} ₽')

        if 0 < all_aliases_expense < category_expense:
            result.append(
                f'--Остальное: {category_expense - all_aliases_expense} ₽'
            )

    result.append(
        f'{TAG}Общая сумма трат за выбранный период: '
        f'{BOLD_TAG_START}{total_expense}₽{BOLD_TAG_END}'
    )

    if output_mode == OutputMode.GOOGLE_SHEETS:
        return result
    return TAG.join(result)


def get_interval_label(time_interval: TimeInterval):
    """Возвращает начало отсчета и текст заголовка."""

    now = datetime.now()
    if time_interval == TimeInterval.MONTH:
        start_time = now - timedelta(days=30)
        return start_time, (
            f'с {start_time.strftime(Config.DATE_FORMAT)} '
            f'по {now.strftime(Config.DATE_FORMAT)}'
        )
    elif time_interval == TimeInterval.YEAR:
        start_time = now - timedelta(days=365)
        return start_time, (
            f'с {start_time.strftime(Config.DATE_FORMAT)} '
            f'по {now.strftime(Config.DATE_FORMAT)}'
        )
    elif time_interval == TimeInterval.TOTAL:
        return datetime.min, 'за все время'
