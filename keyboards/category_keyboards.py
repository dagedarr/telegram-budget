from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from utils.categories import (AliasesCategoryCallbackData,
                              CategoryActionsCallbackData,
                              CategoryDetailsCallbackData)
from utils.paginator import Paginator


def categories_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура меню Категории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Мои Категории',
            callback_data='categories_list',
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Добавить Категорию',
            callback_data='get_category_from_user',
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='other',
        )
    )
    return builder.as_markup()


def add_category_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура создания Категории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Добавить Категорию',
            callback_data='get_category_from_user',
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='category_menu',
        )
    )
    return builder.as_markup()


def categories_list_keyboard(callback, user_categories) -> Paginator:
    """Пагинированый список Категорий."""

    buttons = [
        (
            category.title,
            CategoryDetailsCallbackData(
                category_id=category.id,
            ).pack(),
        )
        for category in user_categories
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
            callback_data='category_menu',
        )
    ])
    return paginator


def confirm_delete_category_keyboard(category_id: int) -> InlineKeyboardMarkup:
    """Клавиатура подтверждения удаления Категории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Удалить',
            callback_data=CategoryActionsCallbackData(
                action='delete_category',
                category_id=category_id
            ).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Отмена',
            callback_data='category_menu',
        )
    )
    return builder.as_markup()


def get_category_title_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения названия Категории."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Подтвердить',
            callback_data='update_category_title',
        ),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='category_menu',
        )
    )
    return builder.as_markup()


def go_to_new_category_keyboard(new_title, category) -> InlineKeyboardMarkup:
    """Клавиатура перехода к новой Категорию."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=f'Перейти к "{new_title}"',
            callback_data=CategoryDetailsCallbackData(
                category_id=category.id,
            ).pack(),
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='category_menu',
        )
    )
    return builder.as_markup()


def get_cat_title_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура перехода к новой Категорию."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Создать',
            callback_data='set_category_title'
        ),
        InlineKeyboardButton(
            text='Отмена',
            callback_data='category_menu',
        )
    )

    return builder.as_markup()


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
