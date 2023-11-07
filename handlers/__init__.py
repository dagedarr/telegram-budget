from aiogram import Router

from utils import paginator_router

from .aliases_handler import router as aliases_router
from .categories_handler import router as category_router
from .change_info_handler import router as change_info_router
from .commands_handler import router as command_router
from .main_handler import router as main_router
from .registration_handler import router as registration_router
from .statistic_handler import router as statistic_router

handlers_router = Router()

handlers_router.include_routers(
    paginator_router,
    change_info_router,
    command_router,
    registration_router,
    category_router,
    statistic_router,
    aliases_router,
    main_router,
)
