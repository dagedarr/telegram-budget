from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.categories import CategoryActionsCallbackData


def category_details_keyboard(category_title: str) -> InlineKeyboardMarkup:
    """Клавиатура Категории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Алиасы',
            callback_data='category_aliases',
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Переименовать',
            callback_data=CategoryActionsCallbackData(
                action='rename_category',
                title=category_title
            ).pack()
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data=CategoryActionsCallbackData(
                action='confirm_delete_category',
                title=category_title
            ).pack(),
        ),
    ),
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='categories_list',
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='В меню',
            callback_data='category_menu',
        )
    )
    return builder.as_markup()
