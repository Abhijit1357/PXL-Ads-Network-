from aiogram import Router
from .profile import router as profile_router
from .panels import router as panels_router
from .general import router as general_router
from .publisher_panel import router as publisher_panel_router
from .register import router as register_router   # <-- Register router import

inline_callbacks_router = Router()

inline_callbacks_router.include_router(profile_router)
inline_callbacks_router.include_router(panels_router)
inline_callbacks_router.include_router(general_router)
inline_callbacks_router.include_router(publisher_panel_router)
inline_callbacks_router.include_router(register_router)  # <-- Register router included here
inline_callbacks_router.include_router(dashboard_router)  # Register dashboard router
