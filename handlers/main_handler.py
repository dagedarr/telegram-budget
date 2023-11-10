from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from config import Config
from core.crud import get_by_attributes, remove
from filters import IsEndOnboardingFilter
from keyboards import (back_to_menu_keyboard, main_keyboard, other_keyboard,
                       universal_keyboard)
from models import Transaction
from utils.transactions import (amount_validate, create_transaction,
                                get_category_or_alias_id,
                                get_transactions_message,
                                parse_text_for_amount_and_category)
from utils.user_actions import callback_message

router = Router(name='main_router')


@router.callback_query(F.data == 'main')
async def main(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает основные функции бота."""

    await state.clear()
    await callback_message(
        target=callback,
        text='Основной функционал бота',
        reply_markup=main_keyboard()
    )


@router.callback_query(F.data == 'latest_transactions')
async def latest_transactions(callback: CallbackQuery, session: AsyncSession):
    """Выводит посление N транзакций пользователя."""

    transactions = await get_by_attributes(
        model=Transaction,
        attributes={
            'user_id': callback.from_user.id
        },
        session=session,
        get_multi=True,
        amount=Config.LATEST_TRANSACTIONS_NUM,
        order_by='date'
    )
    text = await get_transactions_message(transactions=transactions)
    await callback_message(
        target=callback,
        text=text,
        reply_markup=back_to_menu_keyboard()
    )


@router.callback_query(F.data == 'del_last_transaction')
async def del_last_transaction(callback: CallbackQuery, session: AsyncSession):
    """Удаляет последнюю транзакцию пользователя."""

    last_transaction = await get_by_attributes(
        model=Transaction,
        attributes={
            'user_id': callback.from_user.id
        },
        order_by='date',
        session=session,
    )
    if not last_transaction:
        await callback_message(
            target=callback,
            text='У Вас нет истории Трат!',
            reply_markup=back_to_menu_keyboard()
        )
        return

    await remove(
        db_obj=last_transaction,
        session=session
    )

    await callback_message(
        target=callback,
        text=f'Трата "{last_transaction}" успешно удалена!',
        reply_markup=back_to_menu_keyboard()
    )


@router.callback_query(F.data == 'other')
async def other(callback: CallbackQuery):
    """Выводит Категории и Статистику, и остальной функционал."""

    await callback_message(
        target=callback,
        text='Просмотр Категории и Статистики',
        reply_markup=other_keyboard(),
        replace_message=True
    )


@router.message(IsEndOnboardingFilter(), F.text)
async def get_transactions(message: Message, session: AsyncSession):
    """
    Обработчик Транзакций пользователя.
    Создает Транзакцию по введененным значениям суммы и категории (алиаса).

    Пример корректных запросов:
        Продукты 100
        850 Снятие наличных
        990,50 Развлечения
        Транспорт 99.99
    """

    amount, title = await parse_text_for_amount_and_category(
        text=message.text
    )
    if not await amount_validate(amount=amount, message=message):
        return

    if not title:
        await callback_message(
            target=message,
            text='Я не смог обнаружить Категорию в вашем сообщении :(',
            delete_reply=False
        )
        return

    category_or_alias_id = await get_category_or_alias_id(
        title=title,
        message=message,
        session=session
    )

    if category_or_alias_id is None:
        await callback_message(
            target=message,
            text='Категория или Алиас с таким названием не найдены :(\n'
                 'Создайте ее или попрубуйте ввести название еще раз!',
            reply_markup=universal_keyboard([('Создать', 'category_menu')]),
            delete_reply=False
        )
        return

    new_transaction = await create_transaction(
        session=session,
        user_id=message.from_user.id,
        category_id=category_or_alias_id[0],
        alias_id=category_or_alias_id[1],
        amount=amount
    )
    await callback_message(
        target=message,
        text=f'Трата "{new_transaction}" успешно записана!',
        delete_reply=False
    )
