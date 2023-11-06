from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models import Category
from utils.categories import CategoryActionsCallbackData


def category_details_keyboard(category: Category) -> InlineKeyboardMarkup:
    """Клавиатура Категории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Алиасы',
            callback_data='aliases_menu',
            # callback_data=CategoryActionsCallbackData(
            #     action='aliases_menu',
            #     title=category
            # ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Переименовать',
            callback_data=CategoryActionsCallbackData(
                action='rename_category',
                # title=category.title
                category_id=category.id
            ).pack()
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data=CategoryActionsCallbackData(
                action='confirm_del_cat',
                # title=category.title
                category_id=category.id
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
