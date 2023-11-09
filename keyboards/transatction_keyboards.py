from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.transactions import TransactionCallbackData


def confirm_delete_transaction_keyboard(
    transaction_id: int
) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления Транзакции."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Подтвердить',
            callback_data=TransactionCallbackData(
                trans_id=transaction_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='main'
        )
    )
    return builder.as_markup()
