from re import compile

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_by_id, remove
from filters import IsEndOnboardingFilter
from keyboards import (back_to_menu_keyboard,
                       confirm_delete_transaction_keyboard, universal_keyboard)
from models import Transaction
from utils.transactions import (TransactionCallbackData,
                                validate_transaction_for_del)
from utils.user_actions import callback_message, make_onboarding_end

router = Router(name='cmd_router')


@router.message(IsEndOnboardingFilter(), Command(commands=['start']))
async def cmd_start_onboarding(message: Message, session: AsyncSession):
    """Обработчик команды /start для завершенного онбординга."""

    keyboard = universal_keyboard([('Меню', 'main')])

    await make_onboarding_end(
        user_id=message.from_user.id,
        session=session,
        default_username=message.from_user.username
    )
    await message.answer(
        text='Основное меню. Команды можно посмотреть нажав на /help',
        reply_markup=keyboard
    )


@router.message(Command(commands=['start']))
async def cmd_start(message: Message):
    """Обработчик команды /start для нового пользователя."""

    keyboard = universal_keyboard([('Ввести сведения о себе', 'registration')])
    await message.answer(
        text=f'Привет, {message.chat.full_name}, я бот-помощник для ведения '
        'расходов, давай знакомиться! Если хочешь узнать обо мне поподробнее, '
        'нажми на /help чтобы посмотреть функционал!',
        reply_markup=keyboard,
    )


@router.message(Command(commands=['help']))
async def cmd_help(message: Message):
    await message.answer(
        'FIXME'
    )


@router.message(IsEndOnboardingFilter(), Command(compile(r'del_tr')))
async def confirm_delete_user_transaction(
    message: Message,
    session: AsyncSession
):
    """Подтверждает удаление транзакции пользователя."""

    transaction_id_from_msg = message.text.split('/del_tr')[1]

    transaction = await get_by_id(
        model=Transaction,
        obj_id=transaction_id_from_msg,
        session=session
    )

    error_msg = await validate_transaction_for_del(
        transaction_id_from_msg=transaction_id_from_msg,
        transaction=transaction,
        user_id=message.from_user.id
    )

    if error_msg:
        await message.answer(
            error_msg
        )
        return

    await message.answer(
        f'Удалить {transaction}?',
        reply_markup=confirm_delete_transaction_keyboard(
            transaction_id=transaction.id
        ),
    )


@router.callback_query(TransactionCallbackData.filter())
async def delete_user_transaction_by_id(
    callback: CallbackQuery,
    session: AsyncSession,
    callback_data: TransactionCallbackData
):
    """Удаляет транзакцию пользователя по id."""

    transaction = await get_by_id(
        model=Transaction,
        obj_id=callback_data.trans_id,
        session=session
    )
    await remove(
        db_obj=transaction,
        session=session
    )

    await callback_message(
        target=callback,
        text=f'Транзакция {transaction} Успешно удалена!',
        reply_markup=back_to_menu_keyboard()
    )
