from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from keyboards import main_keyboard, other_keyboard
from utils.user_actions import callback_message
from sqlalchemy.ext.asyncio import AsyncSession
from utils.transactions import parse_text_for_amount_and_category


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

    amount, cat_title = await parse_text_for_amount_and_category(
        text=message.text
    )

    print(f'Сумма: "{amount}"\nКатегория: "{cat_title}"')

    # transaction = float(message.text)
    # await create(
    #     session=session,
    #     model=Transaction,
    #     user_id=message.from_user.id,
    #     date=datetime.now().timestamp(),
    #     category_id=1,
    #     amount=transaction
    # )
