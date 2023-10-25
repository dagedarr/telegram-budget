from aiogram import Router

from .change_info_handler import router as change_info_router
from .commands_handler import router as command_router
from .main_handler import router as main_router
from .registration_handler import router as registration_router


handlers_router = Router()

handlers_router.include_routers(
    change_info_router,
    main_router,
    command_router,
    registration_router,
)
