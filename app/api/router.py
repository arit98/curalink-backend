from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.trials import router as trials_router
from app.api.v1.publications import router as publications_router
from app.api.v1.experts import router as experts_router
from app.api.v1.favourites import router as favourites_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(trials_router, prefix="/trials", tags=["trials"])
api_router.include_router(publications_router, prefix="/publications", tags=["publications"])
api_router.include_router(experts_router, prefix="/experts", tags=["experts"])
api_router.include_router(favourites_router, prefix="/favourites", tags=["favourites"])