import contextlib
from typing import Optional, Union

from aiogram import Router, types
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

paginator_router = Router()


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Стандартый синглтон паттер, только через message ID."""

        if 'paginator_id' not in kwargs:
            raise ValueError(
                'Не передан paginator_id в kwargs для инициализации Paginator'
            )
        paginator_id: list = kwargs['paginator_id']

        if len(cls._instances.keys()) > 1000:
            for key in cls._instances.keys()[:300]:
                cls._instances.pop(key)

        if paginator_id not in cls._instances:
            cls._instances[paginator_id] = super(
                MetaSingleton, cls
            ).__call__(*args, **kwargs)

        return cls._instances[paginator_id]


class PaginatorCallbackFactory(CallbackData, prefix='paginator'):
    next: Optional[bool] = None
    paginator_id: int


class Paginator(metaclass=MetaSingleton):
    def __init__(
        self,
        data: list[str] = None,
        page: int = 0,
        dynamic_buttons: list[tuple[str, str | CallbackData]] = False,
        items_on_page: int = 1,
        buttons_adjust: int = 2,
        dynamic_buttons_items_in_page: int = 3,
        dynamic_buttons_items_in_rows: int = 1,
        **kwargs,
    ):
        super().__init__()
        if data is None and not dynamic_buttons:
            raise ValueError(
                'Не передан data/dynamic_buttons для инициализации Paginator'
            )

        self.buttons_adjust = buttons_adjust
        self.dynamic_buttons_items_in_page = dynamic_buttons_items_in_page
        self.dynamic_buttons_items_in_rows = dynamic_buttons_items_in_rows
        self.page = page
        self.items_on_page = (
            items_on_page
            if not dynamic_buttons
            else dynamic_buttons_items_in_page
        )
        if data is None:
            data = [text for text, button_name in dynamic_buttons]
        self.data = self._create_chunks(data)
        self.dynamic_buttons = (
            self._create_chunks(dynamic_buttons)
            if dynamic_buttons
            else False
        )

        self.paginator_id = kwargs.get('paginator_id')
        self.buttons: list[InlineKeyboardButton] = []

    def get_page(self, message_text: str = '', custom_text=None):
        """Генерация текста сообщения."""

        if custom_text:
            page_text = f'{custom_text}\n'
        else:
            page_text = ''
        if self.data:
            for counter, item in enumerate(self.data[self.page]):
                item_in_data_number = counter + (
                    self.items_on_page * self.page
                )
                page_text += f'{item_in_data_number + 1}. {item}\n'

        text = message_text if self.dynamic_buttons else page_text
        if not text:
            text = self.data[0][0]
        return text

    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        """Создание кнопок пагинатора."""

        builder = InlineKeyboardBuilder()
        self._add_basic_buttons(builder)
        builder.adjust(3)

        builder = self._add_custom_buttons(builder)

        return builder.as_markup()

    def add_buttons(
        self,
        buttons: Union[
            InlineKeyboardBuilder,
            list[InlineKeyboardButton],
            InlineKeyboardMarkup,
        ],
    ) -> list[InlineKeyboardButton]:
        """Добавления статичных кнопок."""

        inline_keyboard = []
        if isinstance(buttons, InlineKeyboardBuilder):
            inline_keyboard = buttons.as_markup().inline_keyboard
        elif isinstance(buttons, InlineKeyboardMarkup):
            inline_keyboard = buttons.inline_keyboard
        elif isinstance(buttons, list):
            for button in buttons:
                self.buttons.append(button)
            return
        for line_button in inline_keyboard:
            for button in line_button:
                self.buttons.append(button)

    def _add_custom_buttons(
        self, builder: InlineKeyboardBuilder
    ) -> InlineKeyboardBuilder:
        """Добавляет все кнопки, кроме базовых."""

        basic_buttons: list[
            InlineKeyboardButton
        ] = builder.as_markup().inline_keyboard[0]
        builder = InlineKeyboardBuilder()
        row_buttons = [basic_buttons]
        for counter in range(0, len(self.buttons), self.buttons_adjust):
            line_buttons = []
            for i in range(counter, counter + self.buttons_adjust):
                if i < len(self.buttons):
                    line_buttons.append(self.buttons[i])
            if line_buttons:
                row_buttons.append(line_buttons)

        if self.dynamic_buttons:
            dynamic_buttons_builder = self._build_dynamic_buttons()
            builder.attach(dynamic_buttons_builder)

        for buttons in row_buttons:
            builder.row(*buttons, width=len(buttons))

        return builder

    def _add_basic_buttons(self, builder: InlineKeyboardBuilder):
        """Добавление базовых кнопок."""

        builder.button(
            text='Назад',
            callback_data=PaginatorCallbackFactory(
                next=False, paginator_id=self.paginator_id
            ),
        )
        builder.button(
            text=f'{self.page + 1}/{len(self.data)}',
            callback_data=PaginatorCallbackFactory(
                paginator_id=self.paginator_id
            ),
        )
        builder.button(
            text='Вперед',
            callback_data=PaginatorCallbackFactory(
                next=True, paginator_id=self.paginator_id
            ),
        )

    def _create_chunks(self, array, buttons=False):
        """Разбитие любого массива на требуемые чанки."""

        return [
            array[i: i + self.items_on_page]
            for i in range(0, len(array), self.items_on_page)
        ]

    def _build_dynamic_buttons(self) -> list[InlineKeyboardButton]:
        """Добавление динамический кнопок."""

        builder = InlineKeyboardBuilder()
        all_buttons = []
        for name, callback in self.dynamic_buttons[self.page]:
            all_buttons.append(
                InlineKeyboardButton(text=name, callback_data=callback)
            )
        buttons_row = []
        for counter in range(
            0, len(all_buttons), self.dynamic_buttons_items_in_page
        ):
            line_buttons = []
            for i in range(counter, self.dynamic_buttons_items_in_page):
                if i < len(all_buttons):
                    line_buttons.append(all_buttons[i])
            if line_buttons:
                buttons_row.append(line_buttons)

        for buttons in buttons_row:
            builder.row(*buttons, width=len(buttons))

        buttons = list(builder.buttons)
        builder = InlineKeyboardBuilder()
        buttons = [
            buttons[i: i + self.dynamic_buttons_items_in_rows]
            for i in range(
                0, len(buttons), self.dynamic_buttons_items_in_rows
            )
        ]
        for row in buttons:
            builder.row(*row, width=len(row))
        return builder


@paginator_router.callback_query(PaginatorCallbackFactory.filter())
async def paginator_callback_handler(
    callback: types.CallbackQuery, callback_data: PaginatorCallbackFactory
):
    """Обработка нажатий на базовые кнопки пагинатора."""

    try:
        paginator = Paginator(paginator_id=callback_data.paginator_id)
    except ValueError:
        return
    if callback_data.next is None:
        return

    if callback_data.next:
        paginator.page += (
            1
            if paginator.page != len(paginator.data) - 1
            else -paginator.page
        )
    else:
        paginator.page = (
            paginator.page - 1
            if paginator.page != 0
            else len(paginator.data) - 1
        )

    with contextlib.suppress(TelegramBadRequest):
        await callback.message.edit_text(
            reply_markup=paginator.keyboard,
            text=callback.message.text,
        )
