from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_by_id, get_or_create, update
from forms import RegistrationForm
from keyboards import set_info_keyboard, universal_keyboard
from models import User
from utils.user_actions import callback_message, make_onboarding_end

router = Router(name='registration_router')

# ------------------------ REGISTRATION ------------------------


@router.callback_query(F.data == 'registration')
async def registration(callback: CallbackQuery, session: AsyncSession):
    """Регистрация пользователя."""

    await get_or_create(
        model=User,
        session=session,
        id=callback.from_user.id,
    )
    default_username = callback.from_user.username

    await callback_message(
        target=callback,
        text='Введите данные о себе чтобы мы всегда были на связи.\n'
        f'Также вы можете изменить имя "{default_username}" на другое',
        reply_markup=set_info_keyboard(is_onboarding=True),
    )

# ------------------------ MAIL ------------------------


@router.callback_query(F.data == 'get_mail')
async def get_mail(callback: CallbackQuery, state: FSMContext):
    """Устанавливает state для получения почты."""

    await state.clear()
    await state.set_state(RegistrationForm.mail)
    await callback_message(
        target=callback,
        text='Введите свою почту'
    )


@router.message(RegistrationForm.mail)
async def get_mail_from_message(message: Message, state: FSMContext):
    """Получает почту из сообщения."""

    await state.update_data(mail=message.text)
    keyboard = universal_keyboard(
        [
            ('Установить', 'set_mail'),
            ('Отмена', 'registration')
        ],
        buttons_per_row=2,
    )
    await message.answer(
        text=f'Установить почту: {message.text}?',
        reply_markup=keyboard,
    )


@router.callback_query(F.data == "set_mail", RegistrationForm.mail)
async def set_mail(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Устанавливает почту в БД"""

    keyboard = universal_keyboard(
        [
            ('Поменять имя', 'get_username'),
            ('Назад', 'registration'),
            ('Завершить регистрацию', 'registration_end')
        ],
        buttons_per_row=2,
    )
    state_data = await state.get_data()
    mail = state_data.get('mail')

    await update(
        db_obj=await get_by_id(User, callback.from_user.id, session),
        obj_in={'email': mail},
        session=session
    )
    await state.clear()
    await callback_message(
        target=callback,
        text=f'Почта установлена как "{mail}"',
        reply_markup=keyboard,
    )

# ------------------------ USERNAME ------------------------


@router.callback_query(F.data == 'get_username')
async def get_username(callback: CallbackQuery, state: FSMContext):
    """Устанавливает state для получения имени."""

    await state.clear()
    await state.set_state(RegistrationForm.username)
    await callback_message(
        target=callback,
        text='Введите свое имя'
    )


@router.message(RegistrationForm.username)
async def get_name_from_message(message: Message, state: FSMContext):
    """Получает имя из сообщения."""

    await state.update_data(username=message.text)
    keyboard = universal_keyboard(
        [
            ('Установить', 'set_username'),
            ('Отмена', 'registration')
        ],
        buttons_per_row=2,
    )
    await message.answer(
        text=f'Установить имя: {message.text}?',
        reply_markup=keyboard,
    )


@router.callback_query(F.data == 'set_username', RegistrationForm.username)
async def set_username(
    callback: CallbackQuery, session: AsyncSession, state: FSMContext
):
    """Устанавливает имя в БД"""

    keyboard = universal_keyboard(
        [
            ('Поменять почту', 'get_mail'),
            ('Назад', 'registration'),
            ('Завершить регистрацию', 'registration_end')
        ],
        buttons_per_row=2,
    )
    state_data = await state.get_data()
    username = state_data.get('username')

    await update(
        db_obj=await get_by_id(User, callback.from_user.id, session),
        obj_in={'username': username},
        session=session
    )
    await state.clear()
    await callback_message(
        target=callback,
        text=f'Имя установлено как "{username}"',
        reply_markup=keyboard,
    )

# ------------------------ REGISTRATION END ------------------------


@router.callback_query(F.data == 'registration_end')
async def registration_end(callback: CallbackQuery, session: AsyncSession):
    """Финальное сообщение регистрации."""

    keyboard = universal_keyboard([
        ('Меню', 'main')
    ])
    user_id = callback.from_user.id
    user = await get_by_id(
        model=User,
        session=session,
        obj_id=user_id,
    )
    await make_onboarding_end(
        user_id=user_id,
        session=session,
        default_username=callback.from_user.username
    )
    await callback_message(
        target=callback,
        text=f'Регистрация завершена! {user.username}, '
             'спасибо за регистрацию!',
        reply_markup=keyboard
    )
