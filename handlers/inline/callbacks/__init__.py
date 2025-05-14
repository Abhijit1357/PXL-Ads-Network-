from .profile import router as profile_router
from .panels import router as panels_router
from .general import router as general_router

router = Router()
router.include_router(profile_router)
router.include_router(panels_router)
router.include_router(general_router)
