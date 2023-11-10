from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_by_id, update
from filters import IsEndOnboardingFilter
from forms import RegistrationForm
from keyboards import set_info_keyboard, universal_keyboard
from models import User
from utils.user_actions import callback_message

router = Router(name='change_info_router')


@router.callback_query(F.data == 'change_info')
async def change_info(callback: CallbackQuery):
    """Выводит Категории и Статистику и осльной функционал."""

    await callback_message(
        target=callback,
        text='Изменить данные о себе',
        reply_markup=set_info_keyboard(),
    )


@router.message(IsEndOnboardingFilter(), RegistrationForm.mail)
async def get_mail_from_message(message: Message, state: FSMContext):
    """Получает почту из сообщения."""

    await state.update_data(mail=message.text)
    keyboard = universal_keyboard(
        [
            ('Установить', 'set_mail'),
            ('Отмена', 'change_info')
        ],
        buttons_per_row=2,
    )
    await message.answer(
        text=f'Установить почту: {message.text}?',
        reply_markup=keyboard,
    )


@router.callback_query(
    IsEndOnboardingFilter(),
    F.data == 'set_mail',
    RegistrationForm.mail
)
async def set_mail(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Устанавливает почту в БД."""

    keyboard = universal_keyboard(
        [
            ('Поменять имя', 'get_username'),
            ('Вернуться в меню', 'main')
        ],
        buttons_per_row=1,
    )
    state_data = await state.get_data()
    mail = state_data.get('mail')

    await update(
        db_obj=await get_by_id(User, callback.from_user.id, session),
        obj_in={'email': mail},
        session=session
    )
    await callback_message(
        target=callback,
        text=f'Почта установлена как "{mail}"',
        reply_markup=keyboard,
    )
    await state.clear()


@router.message(IsEndOnboardingFilter(), RegistrationForm.username)
async def get_name_from_message(message: Message, state: FSMContext):
    """Получает имя из сообщения."""

    await state.update_data(username=message.text)
    keyboard = universal_keyboard(
        [
            ('Установить', 'set_username'),
            ('Отмена', 'change_info')
        ],
        buttons_per_row=2,
    )
    await message.answer(
        text=f'Установить имя: {message.text}?',
        reply_markup=keyboard,
    )


@router.callback_query(
    IsEndOnboardingFilter(),
    F.data == 'set_username',
    RegistrationForm.username
)
async def set_username(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Устанавливает имя в БД."""

    keyboard = universal_keyboard(
        [
            ('Поменять почту', 'get_mail'),
            ('Вернуться в меню', 'main')
        ],
        buttons_per_row=1,
    )
    state_data = await state.get_data()
    username = state_data.get('username')

    await update(
        db_obj=await get_by_id(User, callback.from_user.id, session),
        obj_in={'username': username},
        session=session
    )
    await callback_message(
        target=callback,
        text=f'Имя установлено как "{username}"',
        reply_markup=keyboard,
    )
    await state.clear()
