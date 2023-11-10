from typing import List, Tuple, Union

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def universal_keyboard(
    buttons: List[Tuple[str, Union[str, CallbackData]]],
    buttons_per_row: int = 1,
) -> InlineKeyboardMarkup:
    """Универсальная клавиатура с кнопками колбека."""

    builder = InlineKeyboardBuilder()

    if len(buttons) == 1:
        text, data = buttons[0]
        builder.add(InlineKeyboardButton(text=text, callback_data=data))
    else:
        line = []
        for text, data in buttons:
            line.append(
                InlineKeyboardButton(text=text, callback_data=data)
            )
        builder.add(*line)
        builder.adjust(buttons_per_row)
    return builder.as_markup()


def main_keyboard() -> InlineKeyboardMarkup:
    """Основная клавиатура пользователя."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Удалить последнюю трату',
            callback_data='del_last_transaction'
        ),
        InlineKeyboardButton(
            text='Последние траты',
            callback_data='latest_transactions'
        ),
    ),
    builder.row(
        InlineKeyboardButton(
            text='Остальное',
            callback_data='other'
        )
    )

    return builder.as_markup()


def other_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура "Остальное"."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Категории', callback_data='category_menu'
        ),
        InlineKeyboardButton(
            text='Статистика', callback_data='statistic_menu'
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text='Изменить данные о себе', callback_data='change_info'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Связаться с разработчиком', url='https://t.me/nilotan',
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад', callback_data='main'
        )
    )
    return builder.as_markup()


def set_info_keyboard(is_onboarding=False) -> InlineKeyboardMarkup:
    """Клавиатура изменения данных пользователя."""

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='Ввести почту' if is_onboarding else 'Поменять почту',
        callback_data='get_mail')
    )
    builder.add(InlineKeyboardButton(
        text='Поменять имя',
        callback_data='get_username')
    )
    if is_onboarding:
        builder.add(InlineKeyboardButton(
            text='Завершить регистрацию',
            callback_data='registration_end')
        )
    else:
        builder.add(InlineKeyboardButton(
            text='Назад',
            callback_data='other')
        )
    builder.adjust(2)
    return builder.as_markup()


def back_to_menu_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура возврата в основное меню."""

    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text='Вернуться в меню',
        callback_data='main')
    )
    return builder.as_markup()
