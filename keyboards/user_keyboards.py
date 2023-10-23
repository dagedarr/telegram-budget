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



def main_keyboard():
    """
    Основная клавиатура пользователя.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить последнюю трату", callback_data="events_menu"
        ),
        InlineKeyboardButton(text="Последние траты", callback_data="discounts"),
    ),
    builder.row(
        InlineKeyboardButton(
            text="Категории", callback_data="knowledge_base"
        ),
        InlineKeyboardButton(
            text="Статистика", callback_data="about_self"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="Остальное", callback_data="onboarding_msg_7"
        )
    )
    return builder.as_markup()

def main_keyboard():
    """
    Основная клавиатура пользователя.
    """
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text="Удалить последнюю трату", callback_data="events_menu"
        ),
        InlineKeyboardButton(text="Последние траты", callback_data="discounts"),
    ),
    builder.row(
        InlineKeyboardButton(
            text="Категории", callback_data="knowledge_base"
        ),
        InlineKeyboardButton(
            text="Статистика", callback_data="about_self"
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text="Остальное", callback_data="onboarding_msg_7"
        )
    )
    return builder.as_markup()
