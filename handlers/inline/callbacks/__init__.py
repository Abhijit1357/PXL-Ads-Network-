from .register import router as register_router

inline_callbacks_router = Router()
inline_callbacks_router.include_router(profile_router)
inline_callbacks_router.include_router(panels_router)
inline_callbacks_router.include_router(general_router)
inline_callbacks_router.include_router(publisher_panel_router)
inline_callbacks_router.include_router(register_router)  # <---- add this line
