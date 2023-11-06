from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.categories import (AliasesActionsCallbackData,
                              AliasesCategoryCallbackData,
                              CategoryActionsCallbackData,
                              CategoryDetailsCallbackData)


def category_details_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Клавиатура Категории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Алиасы',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_menu',
                category_id=category_id,
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Переименовать',
            callback_data=CategoryActionsCallbackData(
                action='rename_category',
                category_id=category_id
            ).pack()
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data=CategoryActionsCallbackData(
                action='confirm_del_cat',
                category_id=category_id
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


def aliases_menu_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Клавиатура меню Алиасов конкретной категории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Список Алиасов',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_list',
                category_id=category_id
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Добавить Алиас',
            callback_data=AliasesCategoryCallbackData(
                    action='get_alias_from_user',
                    category_id=category_id
            ).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=CategoryDetailsCallbackData(
                category_id=category_id,
            ).pack(),
        ),
        InlineKeyboardButton(
            text='В меню',
            callback_data='category_menu',
        )
    )
    return builder.as_markup()


def alias_details_keyboard(
    alias_id: int,
    category_id: int
) -> InlineKeyboardMarkup:
    """Клавиатура Алиаса."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Удалить',
            callback_data=AliasesActionsCallbackData(
                action='confirm_del_alias',
                alias_id=alias_id,
                category_id=category_id
            ).pack(),
        ),
    ),
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_list',
                category_id=category_id
            ).pack()
        ),
        InlineKeyboardButton(
            text='В меню',
            callback_data='category_menu',
        )
    )
    return builder.as_markup()
