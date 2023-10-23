from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_by_id
from filters import IsEndOnboardingFilter
from keyboards import universal_keyboard, main_keyboard
from models import User
from utils.user_actions import make_onboarding_end

router = Router(name="cmd_router")


@router.message(IsEndOnboardingFilter(), Command(commands=["start"]))
async def cmd_start_onboarding(message: Message, session: AsyncSession):
    """Обработчик команды /start для завершенного онбординга"""
    user_id = message.from_user.id
    await make_onboarding_end(
        user_id=user_id,
        session=session,
        default_username=message.from_user.username
    )
    await message.answer(
        text='Основное меню, команды можно посмотреть нажав на /help '
        'или открыв панель слева от чата',
        reply_markup=main_keyboard()
    )


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message):
    keyboard = universal_keyboard(
        [('Ввести сведения о себе', 'registration')]
    )
    await message.answer(
        text=f'Привет, {message.chat.full_name}, я бот-помощник для ведения '
        'расходов, давай знакомиться! Если хочешь узнать обо мне поподробнее, '
        'нажми на /help чтобы посмотреть функционал!',
        reply_markup=keyboard,
    )


@router.message(Command(commands=["help"]))
async def cmd_help(message: Message):
    await message.answer(
        'для ведения расходов, нажми на /help чтобы посмотреть мой функционал!'
    )
