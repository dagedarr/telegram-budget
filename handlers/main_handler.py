from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from keyboards import main_keyboard, other_keyboard
from utils.transactions import (amount_validate, create_transaction,
                                get_category_or_alias_id,
                                parse_text_for_amount_and_category)
from utils.user_actions import callback_message

router = Router(name="main_router")


@router.callback_query(F.data == "main")
async def main(callback: CallbackQuery):
    """Обрабатывает основные функции бота."""
    await callback_message(
        target=callback,
        text='Основной функционал бота',
        reply_markup=main_keyboard()
    )


@router.callback_query(F.data == "other")
async def other(callback: CallbackQuery):
    """Выводит Категории и Статистику и осльной функционал."""
    await callback_message(
        target=callback,
        text='Просмотр Категории и Статистики',
        reply_markup=other_keyboard(),
        replace_message=True
    )


@router.message(F.text)
async def get_transactions(message: Message, session: AsyncSession):
    amount, title = await parse_text_for_amount_and_category(
        text=message.text
    )
    print(f'{amount=}; {title=}')
    if not await amount_validate(amount=amount, message=message):
        return

    if not title:
        # FIXME
        # надо предложить создать категорию или добавить трату в "Категория по умолчанию"
        await callback_message(
            target=message,
            text='Я не смог обнаружить категорию в вашем сообщении',
            delete_reply=False
        )
        return

    category_or_alias_id = await get_category_or_alias_id(
        title=title,
        message=message,
        session=session
    )
    print(category_or_alias_id)
    if category_or_alias_id is None:
        # await create_category_or_alias()
        print('Пустая категория')
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
        text=str(new_transaction),
        delete_reply=False
    )
