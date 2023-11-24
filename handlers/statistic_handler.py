from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_by_id
from filters import IsEndOnboardingFilter
from keyboards import (back_to_menu_keyboard, choose_interval_keyboard,
                       confirm_mail_keyboard, get_statistic_keyboard,
                       statistic_menu_keyboard)
from models import User
from tasks.tasks import (send_email_statistic, set_user_permissions,
                         spreadsheets_create, spreadsheets_update_value)
from utils.statistic import (OutputMode, StatisticCallbackData,
                             get_interval_label, set_statistic_msg)
from utils.user_actions import callback_message

router = Router(name='statistic_router')


@router.message(IsEndOnboardingFilter(), Command(commands=['statistic']))
@router.callback_query(F.data == 'statistic_menu')
async def statistic_menu(callback: CallbackQuery, state: FSMContext):
    """Меню Статистики."""

    await state.clear()

    try:
        await callback_message(
            target=callback,
            text='Основное меню Статистики. Выберите за какой срок '
                 'вы хотите получить информацию.',
            reply_markup=statistic_menu_keyboard()
        )
    except TelegramBadRequest:
        pass


@router.callback_query(
    StatisticCallbackData.filter(F.action == 'statistic_intervals')
)
async def statistic_intervals(
    callback: CallbackQuery,
    callback_data: StatisticCallbackData,
    state: FSMContext
):
    time_interval = callback_data.time_interval
    await state.update_data(time_interval=time_interval)
    await callback_message(
        target=callback,
        text=f'Статистика {get_interval_label(time_interval)[1]}',
        reply_markup=choose_interval_keyboard()
    )


@router.callback_query(F.data == 'send_statistic_to_chat')
async def send_statistic_to_chat(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Вывод Статистики в чат."""

    data = await state.get_data()
    time_interval = data['time_interval']
    await state.clear()

    text = await set_statistic_msg(
        user_id=callback.from_user.id,
        time_interval=time_interval,
        session=session,
        output_mode=OutputMode.TG_CHAT
    )

    await callback_message(
        target=callback,
        text=text,
        reply_markup=get_statistic_keyboard(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'confirm_mail')
async def confirm_mail(
    callback: CallbackQuery,
    session: AsyncSession
):
    """Проверка почты."""

    user = await get_by_id(
        model=User,
        obj_id=callback.from_user.id,
        session=session
    )

    await callback_message(
        target=callback,
        text=f'Отправить на почту {user.email}?',
        reply_markup=confirm_mail_keyboard(),
        parse_mode='HTML'
    )


@router.callback_query(F.data == 'send_statistic_to_email')
async def send_statistic_to_email(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Отправка сообщения Статистики по почте."""

    data = await state.get_data()
    time_interval = data['time_interval']
    await state.clear()

    user = await get_by_id(
        model=User,
        obj_id=callback.from_user.id,
        session=session
    )

    text = await set_statistic_msg(
        user_id=callback.from_user.id,
        time_interval=time_interval,
        session=session,
        output_mode=OutputMode.MAIL
    )
    label = get_interval_label(time_interval)[1]
    send_email_statistic.delay(
        user_email=user.email,
        subject=f'Отчет от telegram-budget {label}',
        text=text
    )

    await callback_message(
        target=callback,
        text=f'Сообщение успешно отправлено на почту "{user.email}"!',
        reply_markup=back_to_menu_keyboard(),
    )


@router.callback_query(F.data == 'send_statistic_as_excel')
async def send_statistic_as_excel(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession
):
    """Отправка ссылки гугл-таблицы со Статистикой."""

    await callback_message(
        target=callback,
        text='Подождите, формируется таблица...',
    )
    data = await state.get_data()
    time_interval = data['time_interval']
    await state.clear()

    # Создание гугл-таблицы
    spreadsheet_id = str(spreadsheets_create.delay(
        label=get_interval_label(time_interval)[1]
    ).get())

    # Выдача прав для исп-я гугл-таблицы
    set_user_permissions.delay(spreadsheet_id)

    table_data = await set_statistic_msg(
        user_id=callback.from_user.id,
        time_interval=time_interval,
        session=session,
        output_mode=OutputMode.GOOGLE_SHEETS
    )

    # Внесение данных в гугл-таблицу
    spreadsheets_update_value.delay(
        spreadsheet_id,
        [[row] for row in table_data],
    )

    await callback_message(
        target=callback,
        text=('Ваша ссылка:\n'
              f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'),
        reply_markup=back_to_menu_keyboard(),
        delete_reply=False
    )
