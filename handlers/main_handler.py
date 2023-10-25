from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy.ext.asyncio import AsyncSession

from core.crud import get_by_id, update
from filters import IsEndOnboardingFilter
from forms.user_form import RegistrationForm
from keyboards import (main_keyboard, other_keyboard, set_info_keyboard,
                       universal_keyboard)
from models import User
from utils.user_actions import callback_message

router = Router(name="main_router")


@router.callback_query(F.data == "main")
async def main(callback: CallbackQuery):
    """Обрабатывает основные функции бота."""
    await callback_message(
        target=callback,
        text='Основной функционал бота',
        reply_markup=main_keyboard()
    )


@router.callback_query(F.data == "other")
async def other(callback: CallbackQuery):
    """Выводит Категории и Статистику и осльной функционал."""
    await callback_message(
        target=callback,
        text='Просмотр Категории и Статистики',
        reply_markup=other_keyboard(),
        replace_message=True
    )

