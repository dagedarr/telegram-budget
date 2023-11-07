from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import universal_keyboard
from utils.user_actions import callback_message
from utils.statistic import StatisticCallbackData

router = Router(name='statistic_router')


@router.callback_query(F.data == 'statistic_menu')
async def statistic_menu(callback: CallbackQuery):
    """Меню Статистики."""

    keyboard = universal_keyboard([
        ('За последний месяц', StatisticCallbackData(time_interval='mounth').pack()),
        ('За последний год', StatisticCallbackData(time_interval='year').pack()),
        ('За все время', StatisticCallbackData(time_interval='total').pack()),
        ('Назад', 'other'),
    ])

    await callback_message(
        target=callback,
        text='Основное меню Статистики',
        reply_markup=keyboard
    )


@router.callback_query(
    StatisticCallbackData.filter()
)
async def statistic_intervals(
    callback: CallbackQuery,
    callback_data: StatisticCallbackData,
    session: AsyncSession
):
    keyboard = universal_keyboard([
        ('Получить в чат', '123'),
        ('Отправить на почту', '123'),
        ('Назад', 'statistic_menu'),
        ('В меню', 'other'),
    ])
    await callback_message(
        target=callback,
        text=callback_data.time_interval,
        reply_markup=keyboard
    )
