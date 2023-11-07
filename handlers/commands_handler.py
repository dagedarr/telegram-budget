from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from filters import IsEndOnboardingFilter
from keyboards import universal_keyboard
from utils.user_actions import make_onboarding_end

router = Router(name='cmd_router')


@router.message(IsEndOnboardingFilter(), Command(commands=['start']))
async def cmd_start_onboarding(message: Message, session: AsyncSession):
    """Обработчик команды /start для завершенного онбординга."""

    keyboard = universal_keyboard([
        ('Меню', 'main')
    ])
    user_id = message.from_user.id
    await make_onboarding_end(
        user_id=user_id,
        session=session,
        default_username=message.from_user.username
    )
    await message.answer(
        text='Основное меню. Команды можно посмотреть нажав на /help',
        reply_markup=keyboard
    )


@router.message(Command(commands=['start']))
async def cmd_start(message: Message):
    """Обработчик команды /start для нового пользователя."""

    keyboard = universal_keyboard(
        [('Ввести сведения о себе', 'registration')]
    )
    await message.answer(
        text=f'Привет, {message.chat.full_name}, я бот-помощник для ведения '
        'расходов, давай знакомиться! Если хочешь узнать обо мне поподробнее, '
        'нажми на /help чтобы посмотреть функционал!',
        reply_markup=keyboard,
    )


@router.message(Command(commands=['help']))
async def cmd_help(message: Message):
    await message.answer(
        'FIXME'
    )
