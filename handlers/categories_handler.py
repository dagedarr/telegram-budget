from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import (get_by_attributes, get_by_id, get_or_create, remove,
                       update)
from forms import CategoryForm, CategoryUpdateForm
from keyboards import (add_category_keyboard, categories_list_keyboard,
                       categories_menu_keyboard, category_details_keyboard,
                       confirm_delete_category_keyboard,
                       get_cat_title_keyboard, get_category_title_keyboard,
                       go_to_new_category_keyboard, universal_keyboard)
from models import Category
from utils.categories import (CategoryActionsCallbackData,
                              CategoryDetailsCallbackData)
from utils.user_actions import callback_message

router = Router(name='category_router')


@router.callback_query(F.data == 'category_menu')
async def category_menu(callback: CallbackQuery, state: FSMContext):
    """Меню Категории."""

    await state.clear()
    await callback_message(
        target=callback,
        text='Основное меню Категории',
        reply_markup=categories_menu_keyboard()
    )


@router.callback_query(F.data == 'categories_list')
async def categories_list(callback: CallbackQuery, session: AsyncSession):
    """Список категорий пользвоателя."""

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
            reply_markup=add_category_keyboard()
        )
        return

    paginator = categories_list_keyboard(callback, user_categories)

    await callback_message(
        target=callback,
        text='Основное меню Категории',
        reply_markup=paginator.keyboard
    )


@router.callback_query(CategoryDetailsCallbackData.filter())
async def category_details(
    callback: CallbackQuery,
    callback_data: CategoryDetailsCallbackData,
    session: AsyncSession
):
    """Меню конкретной Категории."""

    category = await get_by_id(
        model=Category,
        obj_id=callback_data.category_id,
        session=session
    )
    await callback_message(
        target=callback,
        text=f'Меню Категории "{category.title}"',
        reply_markup=category_details_keyboard(category_id=category.id)
    )

# ------------------------ DELETE CATEGORY ------------------------


@router.callback_query(
    CategoryActionsCallbackData.filter(F.action == 'confirm_del_cat')
)
async def confirm_delete_category(
    callback: CallbackQuery,
    callback_data: CategoryActionsCallbackData,
    session: AsyncSession
):
    """Подтверждение удаления Категории."""

    category = await get_by_id(
        model=Category,
        obj_id=callback_data.category_id,
        session=session
    )

    await callback_message(
        target=callback,
        text=f'Вы точно хотите удалить Категорию "{category.title}"',
        reply_markup=confirm_delete_category_keyboard(
            callback_data.category_id
        ),
    )


@router.callback_query(
    CategoryActionsCallbackData.filter(F.action == 'delete_category')
)
async def delete_category(
    callback: CallbackQuery,
    callback_data: CategoryActionsCallbackData,
    session: AsyncSession
):
    """Удаление Категории."""

    category = await get_by_attributes(
        model=Category,
        attributes={
            'id': callback_data.category_id,
            'user_id': callback.from_user.id
        },
        session=session
    )
    await remove(
        db_obj=category,
        session=session
    )

    await callback_message(
        target=callback,
        text=f'Категория "{category.title}" успешно удалена!',
        reply_markup=universal_keyboard([(('В меню', 'category_menu'))]),
    )

# ------------------------ RENAME CATEGORY ------------------------


@router.callback_query(
    CategoryActionsCallbackData.filter(F.action == 'rename_category')
)
async def rename_category(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: CategoryActionsCallbackData,
    session: AsyncSession
):
    """Устанавливает state для получения названия Категории."""

    await state.clear()
    await state.set_state(CategoryUpdateForm.new_title)
    category = await get_by_attributes(
        model=Category,
        attributes={
            'id': callback_data.category_id,
            'user_id': callback.from_user.id
        },
        session=session
    )

    await state.update_data(old_title=category.title)

    await callback_message(
        target=callback,
        text=f'Введите новое название для Категории "{category.title}"'
    )


@router.message(CategoryUpdateForm.new_title)
async def get_new_title_from_message(message: Message, state: FSMContext):
    """Получает новое название Категории из сообщения."""

    await state.update_data(new_title=message.text)
    data = await state.get_data()
    old_title = data.get('old_title')

    await message.answer(
        text=f'Переименовать "{old_title}" -> "{message.text}"?',
        reply_markup=get_category_title_keyboard(),
    )


@router.callback_query(
    F.data == 'update_category_title', CategoryUpdateForm.new_title
)
async def update_category_title(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Обновляет имя Категории в БД если такого названия нет."""

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
            reply_markup=universal_keyboard([('В меню', 'category_menu')]),
        )
        return

    await update(
        db_obj=category,
        obj_in={
            'title': new_title
        },
        session=session
    )

    await callback_message(
        target=callback,
        text='Название успешно изменено!',
        reply_markup=go_to_new_category_keyboard(new_title, category),
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
    await message.answer(
        text=f'Создать Категорию: "{message.text}"?',
        reply_markup=get_cat_title_keyboard(),
    )


@router.callback_query(F.data == 'set_category_title', CategoryForm.title)
async def set_category_title(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Создает Категорию в БД если ее нет."""

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

    category = await get_by_attributes(
        model=Category,
        attributes={
            'user_id': callback.from_user.id,
            'title': category_title
        },
        session=session
    )

    await callback_message(
        target=callback,
        text=text,
        reply_markup=go_to_new_category_keyboard(
            new_title=category_title,
            category=category
        ),
    )
