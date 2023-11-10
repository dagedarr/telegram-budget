from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from utils.categories import (AliasDetailsCallbackData,
                              AliasesActionsCallbackData,
                              AliasesCategoryCallbackData,
                              CategoryDetailsCallbackData)
from utils.paginator import Paginator


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


def add_alias_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Клавиатура добавления Алиаса."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить Алиас',
            callback_data=AliasesCategoryCallbackData(
                action='get_alias_from_user',
                category_id=category_id
            ).pack(),
        ),
    ),
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_menu',
                category_id=category_id
            ).pack()
        )
    )
    return builder.as_markup()


def aliases_list_keyboard(
    callback, category_id, category_aliases
) -> Paginator:
    """Клавиатура пагинированного списка Алиасов."""

    buttons = [
        (
            alias.title,
            AliasDetailsCallbackData(
                alias_id=alias.id,
                category_id=category_id
            ).pack(),
        )
        for alias in category_aliases
    ]
    paginator = Paginator(
        paginator_id=callback.message.message_id,
        dynamic_buttons=buttons,
        dynamic_buttons_items_in_page=Config.PAGINATOR_BUTTONS,
        dynamic_buttons_items_in_rows=1,
    )

    paginator.add_buttons([
        InlineKeyboardButton(
            text='Назад',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_menu',
                category_id=category_id
            ).pack(),
        )
    ])

    return paginator


def confirm_del_alias_keyboard(
    category_id: int, alias_id: int
) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления Алиаса."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Удалить',
            callback_data=AliasesActionsCallbackData(
                action='delete_alias',
                category_id=category_id,
                alias_id=alias_id,
            ).pack()
        ),
    ),
    builder.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_menu',
                category_id=category_id
            ).pack()
        )
    )
    return builder.as_markup()


def delete_alias_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Клавиатура удаления Алиаса."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='В меню',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_menu',
                category_id=category_id
            ).pack()
        ),
    ),
    return builder.as_markup()


def get_alias_title_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения создания Алиаса."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Создать',
            callback_data='set_alias_title'
        ),
        InlineKeyboardButton(
            text='Отмена',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_menu',
                category_id=category_id
            ).pack()
        )
    ),
    return builder.as_markup()


def go_to_alias_keyboard(
    category_id: int, alias_id: int, alias_title: str
) -> InlineKeyboardMarkup:
    """Клавиатура перехода к Алиасу."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f'Перейти к "{alias_title}"',
            callback_data=AliasDetailsCallbackData(
                alias_id=alias_id,
                category_id=category_id
            ).pack()
        ),
    ),
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data=AliasesCategoryCallbackData(
                action='aliases_menu',
                category_id=category_id
            ).pack()
        )
    )
    return builder.as_markup()
