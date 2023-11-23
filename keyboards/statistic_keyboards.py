from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.statistic import StatisticCallbackData, TimeInterval


def statistic_menu_keyboard() -> InlineKeyboardMarkup:
    """Основная клавиатура Статистики."""

    builder = InlineKeyboardBuilder()

    builder.row(
        InlineKeyboardButton(
            text='За последний месяц',
            callback_data=StatisticCallbackData(
                action='statistic_intervals',
                time_interval=TimeInterval.MONTH
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='За последний год',
            callback_data=StatisticCallbackData(
                action='statistic_intervals',
                time_interval=TimeInterval.YEAR
            ).pack()
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='За все время',
            callback_data=StatisticCallbackData(
                action='statistic_intervals',
                time_interval=TimeInterval.TOTAL
            ).pack()
        ),
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='other'
        )
    )
    return builder.as_markup()


def choose_interval_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура выбора интревала расчета Статистики."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Получить в чат',
            callback_data='send_statistic_to_chat'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Отправить на почту',
            callback_data='confirm_mail'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Получить ссылку на таблицу',
            callback_data='send_statistic_as_excel'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='statistic_menu'
        ),
        InlineKeyboardButton(
            text='В меню',
            callback_data='other'
        )
    )
    return builder.as_markup()


def get_statistic_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура перехода после вывода Статистики."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='statistic_menu'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='В меню',
            callback_data='other'
        )
    )
    return builder.as_markup()


def confirm_mail_keyboard() -> InlineKeyboardMarkup:
    """Клавиатура подтверждения почты перед отправкой сообщения."""

    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text='Да',
            callback_data='send_statistic_to_email'
        ),
        InlineKeyboardButton(
            text='Поменять',
            callback_data='get_mail'
        )
    )
    builder.row(
        InlineKeyboardButton(
            text='Назад',
            callback_data='statistic_menu'
        )
    )
    return builder.as_markup()
