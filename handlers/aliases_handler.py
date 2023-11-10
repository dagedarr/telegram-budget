from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_by_attributes, get_by_id, get_or_create, remove
from forms import AliasForm
from keyboards import (add_alias_keyboard, alias_details_keyboard,
                       aliases_list_keyboard, aliases_menu_keyboard,
                       confirm_del_alias_keyboard, delete_alias_keyboard,
                       get_alias_title_keyboard, go_to_alias_keyboard)
from models import Alias, Category
from utils.categories import (AliasDetailsCallbackData,
                              AliasesActionsCallbackData,
                              AliasesCategoryCallbackData)
from utils.user_actions import callback_message

router = Router(name='aliases_router')


@router.callback_query(
    AliasesCategoryCallbackData.filter(F.action == 'aliases_menu')
)
async def aliases_menu(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: AliasesCategoryCallbackData,
    session: AsyncSession
):
    """Меню Алиасов."""

    await state.clear()
    category = await get_by_id(
        model=Category,
        obj_id=callback_data.category_id,
        session=session
    )

    keyboard = aliases_menu_keyboard(callback_data.category_id)
    await callback_message(
        target=callback,
        text=f'Меню Алиасов категории "{category.title}"',
        reply_markup=keyboard
    )


@router.callback_query(
    AliasesCategoryCallbackData.filter(F.action == 'aliases_list')
)
async def aliases_list(
    callback: CallbackQuery,
    session: AsyncSession,
    callback_data: AliasesCategoryCallbackData,
):
    """Список Алиасов выбранной категории."""

    category = await get_by_id(
        model=Category,
        obj_id=callback_data.category_id,
        session=session
    )

    category_aliases = await get_by_attributes(
        model=Alias,
        attributes={
            'user_id': callback.from_user.id,
            'category_id': callback_data.category_id
        },
        session=session,
        get_multi=True
    )
    if not category_aliases:
        await callback_message(
            target=callback,
            text='Вы не добавили к категорию ни одного Алиаса :(',
            reply_markup=add_alias_keyboard(category_id=category.id)
        )
        return

    paginator = aliases_list_keyboard(callback, category.id, category_aliases)

    await callback_message(
        target=callback,
        text=f'Основное меню Алиасов категории "{category.title}"',
        reply_markup=paginator.keyboard
    )


@router.callback_query(AliasDetailsCallbackData.filter())
async def category_details(
    callback: CallbackQuery,
    callback_data: AliasDetailsCallbackData,
    session: AsyncSession
):
    """Меню конкретного Алиаса."""

    alias = await get_by_id(
        model=Alias,
        obj_id=callback_data.alias_id,
        session=session
    )

    await callback_message(
        target=callback,
        text=f'Меню Алиаса "{alias}"',
        reply_markup=alias_details_keyboard(
            alias_id=callback_data.alias_id,
            category_id=callback_data.category_id
        )
    )


# ------------------------ DELETE CATEGORY ------------------------


@router.callback_query(
    AliasesActionsCallbackData.filter(F.action == 'confirm_del_alias')
)
async def confirm_delete_alias(
    callback: CallbackQuery,
    callback_data: AliasesActionsCallbackData,
    session: AsyncSession
):
    """Подтверждение удаления Алиаса."""

    alias = await get_by_id(
        model=Alias,
        obj_id=callback_data.alias_id,
        session=session
    )

    await callback_message(
        target=callback,
        text=f'Вы точно хотите удалить Алиас "{alias}"',
        reply_markup=confirm_del_alias_keyboard(
            category_id=callback_data.category_id,
            alias_id=callback_data.alias_id
        ),
    )


@router.callback_query(
    AliasesActionsCallbackData.filter(F.action == 'delete_alias')
)
async def delete_alias(
    callback: CallbackQuery,
    callback_data: AliasesActionsCallbackData,
    session: AsyncSession
):
    """Удаление Алиаса."""

    alias = await get_by_attributes(
        model=Alias,
        attributes={
            'id': callback_data.alias_id,
            'user_id': callback.from_user.id
        },
        session=session
    )
    await remove(
        db_obj=alias,
        session=session
    )

    await callback_message(
        target=callback,
        text=f'Алиас "{alias}" успешно удален!',
        reply_markup=delete_alias_keyboard(callback_data.category_id)
    )


# ------------------------ ADD ALIAS ------------------------


@router.callback_query(
    AliasesCategoryCallbackData.filter(F.action == 'get_alias_from_user')
)
async def get_alias_from_user(
    callback: CallbackQuery,
    state: FSMContext,
    callback_data: AliasesCategoryCallbackData,
):
    """Устанавливает state для получения названия Алиаса."""

    await state.clear()
    await state.set_state(AliasForm.title)
    await state.update_data(category_id=callback_data.category_id)

    await callback_message(
        target=callback,
        text='Введите название Алиаса'
    )


@router.message(AliasForm.title)
async def get_alias_from_message(message: Message, state: FSMContext):
    """Получает название Алиаса из сообщения."""

    state_data = await state.get_data()
    category_id = state_data.get('category_id')

    await state.update_data(alias_title=message.text)

    await message.answer(
        text=f'Создать Алиас: "{message.text}"?',
        reply_markup=get_alias_title_keyboard(category_id=category_id),
    )


@router.callback_query(F.data == 'set_alias_title', AliasForm.title)
async def set_alias_title(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Создает Алиас в БД если его нет."""

    state_data = await state.get_data()
    alias_title = state_data.get('alias_title')
    category_id = state_data.get('category_id')

    _, is_get = await get_or_create(
        session=session,
        model=Alias,
        user_id=callback.from_user.id,
        title=alias_title,
        category_id=category_id
    )
    await state.clear()

    alias = await get_by_attributes(
        model=Alias,
        attributes={
            'user_id': callback.from_user.id,
            'title': alias_title,
            'category_id': category_id
        },
        session=session
    )

    if is_get:
        text = f'Алиас "{alias_title}" Уже был создан Вами!'
    else:
        text = f'Алиас "{alias_title}" Успешно создан!'

    await callback_message(
        target=callback,
        text=text,
        reply_markup=go_to_alias_keyboard(
            category_id=category_id,
            alias_id=alias.id,
            alias_title=alias_title
        ),
    )
