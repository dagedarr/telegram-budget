from aiogram import F, Router
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession
from aiogram.fsm.context import FSMContext

from keyboards import universal_keyboard, category_details_keyboard
from utils.user_actions import callback_message
from core.crud import get_by_attributes, get_or_create, update
from models import Category
from forms import CategoryForm, CategoryUpdateForm
from utils.paginator import Paginator
from utils.categories import CategoryDetailsCallbackData, CategoryActionsCallbackData


router = Router(name='category_router')


@router.callback_query(F.data == 'category_menu')
async def category_menu(callback: CallbackQuery, state: FSMContext):
    """Меню Категории."""

    await state.clear()
    keyboard = universal_keyboard([
        ('Мои Категории', 'categories_list'),
        ('Добавить Категорию', 'get_category_from_user'),
        ('Назад', 'other')
    ])

    await callback_message(
        target=callback,
        text='Основное меню Категории',
        reply_markup=keyboard
    )


@router.callback_query(F.data == 'categories_list')
async def categories_list(callback: CallbackQuery, session: AsyncSession):
    """Список категорий пользвоателя."""

    keyboard = universal_keyboard(
        [
            ('Добавить Категорию', 'get_category_from_user'),
            ('Назад', 'category_menu')
        ])

    user_categories = await get_by_attributes(
        model=Category,
        attributes={
            'user_id': callback.from_user.id
        },
        session=session,
        get_multi=True
    )
    if not user_categories:
        await callback_message(
            target=callback,
            text='Вы не добавили ни одной категории :(',
            reply_markup=keyboard
        )
        return

    buttons = [
        (
            category.title,
            CategoryDetailsCallbackData(
                category_id=category.id,
                category_title=category.title
            ).pack(),
        )
        for category in user_categories
    ]
    paginator = Paginator(
        paginator_id=callback.message.message_id,
        dynamic_buttons=buttons,
        dynamic_buttons_items_in_page=3,
        dynamic_buttons_items_in_rows=1,
    )

    paginator.add_buttons(
        universal_keyboard([
            ('Назад', 'category_menu')
        ])
    )

    await callback_message(
        target=callback,
        text='Основное меню Категории',
        reply_markup=paginator.keyboard
    )


@router.callback_query(CategoryDetailsCallbackData.filter())
async def category_details(
    callback: CallbackQuery,
    callback_data: CategoryDetailsCallbackData,
):
    title = callback_data.category_title
    await callback_message(
        target=callback,
        text=f'Меню Категории "{title}"',
        reply_markup=category_details_keyboard(category_title=title)
    )


# ------------------------ RENAME CATEGORY ------------------------

@router.callback_query(
    CategoryActionsCallbackData.filter(F.action == 'rename_category')
)
async def rename_category(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: CategoryActionsCallbackData,
):
    """Устанавливает state для получения названия Категории."""

    await state.clear()
    await state.set_state(CategoryUpdateForm.new_title)
    await state.update_data(old_title=callback_data.title)

    await callback_message(
        target=callback,
        text=f'Введите новое название для Категории "{callback_data.title}"'
    )


@router.message(CategoryUpdateForm.new_title)
async def get_new_title_from_message(message: Message, state: FSMContext):
    """Получает новое название Категории из сообщения."""

    await state.update_data(new_title=message.text)
    data = await state.get_data()
    old_title = data.get('old_title')

    keyboard = universal_keyboard(
        [
            ('Подтвердить', 'update_category_title'),
            ('Отмена', 'category_menu')
        ],
        buttons_per_row=2,
    )

    await message.answer(
        text=f'Переименовать "{old_title}" -> "{message.text}"?',
        reply_markup=keyboard,
    )


@router.callback_query(
    F.data == 'update_category_title', CategoryUpdateForm.new_title
)
async def update_category_title(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Обновляет имя Категории в БД."""

    state_data = await state.get_data()
    new_title = state_data.get('new_title')
    old_title = state_data.get('old_title')

    category = await get_by_attributes(
        model=Category,
        attributes={
            'title': old_title,
            'user_id': callback.from_user.id
        },
        session=session
    )

    is_exist = await get_by_attributes(
        model=Category,
        attributes={
            'title': new_title,
            'user_id': callback.from_user.id
        },
        session=session
    )
    await state.clear()
    if is_exist is not None:
        await callback_message(
            target=callback,
            text='Такая Категория уже существет :(',
            reply_markup=universal_keyboard([
                ('В меню', 'category_menu')
            ]),
        )
        return

    await update(
        db_obj=category,
        obj_in={
            'title': new_title
        },
        session=session
    )

    keyboard = universal_keyboard([
        (
            f'Перейти к "{new_title}"',
            CategoryDetailsCallbackData(
                category_id=category.id,
                category_title=category.title
            ).pack()
        ),
        ('Назад', 'category_menu'),
    ])

    await callback_message(
        target=callback,
        text='Название успешно изменено!',
        reply_markup=keyboard,
    )

# ------------------------ ADD CATEGORY ------------------------


@router.callback_query(F.data == 'get_category_from_user')
async def get_category_from_user(
    callback: CallbackQuery,
    state: FSMContext,
):
    """Устанавливает state для получения названия Категории."""

    await state.clear()
    await state.set_state(CategoryForm.title)
    await callback_message(
        target=callback,
        text='Введите название Категории'
    )


@router.message(CategoryForm.title)
async def get_category_from_message(message: Message, state: FSMContext):
    """Получает название Категории из сообщения."""

    await state.update_data(cat_title=message.text)
    keyboard = universal_keyboard(
        [
            ('Создать', 'set_category_title'),
            ('Отмена', 'category_menu')
        ],
        buttons_per_row=2,
    )

    await message.answer(
        text=f'Создать Категорию: "{message.text}"?',
        reply_markup=keyboard,
    )


@router.callback_query(F.data == 'set_category_title', CategoryForm.title)
async def set_category_title(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Создает Категорию в БД."""

    state_data = await state.get_data()
    category_title = state_data.get('cat_title')

    category, is_get = await get_or_create(
        session=session,
        model=Category,
        user_id=callback.from_user.id,
        title=category_title
    )
    await state.clear()

    if is_get:
        text = f'Категория "{category_title}" Уже была создана Вами!'
    else:
        text = f'Категория "{category_title}" Успешно создана!'

    keyboard = universal_keyboard([
        (
            f'Перейти к "{category_title}"',
            CategoryDetailsCallbackData(
                category_id=category.id,
                category_title=category.title
            ).pack()
        ),
        ('Назад', 'category_menu'),
    ])

    await callback_message(
        target=callback,
        text=text,
        reply_markup=keyboard,
    )
