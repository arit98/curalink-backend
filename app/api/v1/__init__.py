from fastapi import APIRouter
from .auth import router as auth_router
from .trials import router as trials_router
from .publications import router as publications_router
from .experts import router as experts_router
from .favourites import router as favourites_router

router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(trials_router, prefix="/trials", tags=["trials"])
router.include_router(publications_router, prefix="/publications", tags=["publications"])
router.include_router(experts_router, prefix="/experts", tags=["experts"])
router.include_router(favourites_router, prefix="/favourites", tags=["favourites"])