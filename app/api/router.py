from fastapi import APIRouter
from app.api.v1.auth import router as auth_router
from app.api.v1.trials import router as trials_router
from app.api.v1.publications import router as publications_router
from app.api.v1.experts import router as experts_router
from app.api.v1.favourites import router as favourites_router
from app.api.v1.onboarding import router as onboarding_router
from app.api.v1.forums import router as forums_router
from app.api.v1.forum.categories import router as forum_categories_router


api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(trials_router, prefix="/trials", tags=["trials"])
api_router.include_router(publications_router, prefix="/publications", tags=["publications"])
api_router.include_router(experts_router, prefix="/experts", tags=["experts"])
api_router.include_router(favourites_router, prefix="/favourites", tags=["favourites"])
api_router.include_router(onboarding_router, prefix="/onboarding", tags=["onboarding"])
api_router.include_router(forums_router, prefix="/forums", tags=["forums"])
api_router.include_router(forum_categories_router, prefix="/forums/categories", tags=["forum-categories"])