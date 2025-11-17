from fastapi import APIRouter
from .auth import router as auth_router
from .trials import router as trials_router
from .publications import router as publications_router
from .experts import router as experts_router
from .favourites import router as favourites_router
from .onboarding import router as onboarding_router
from .forums import router as forums_router
from .forum.categories import router as forum_categories_router
from .forum.reply import router as forum_reply_router
from .pdf import router as pdf_router


router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(trials_router, prefix="/trials", tags=["trials"])
router.include_router(publications_router, prefix="/publications", tags=["publications"])
router.include_router(experts_router, prefix="/experts", tags=["experts"])
router.include_router(favourites_router, prefix="/favourites", tags=["favourites"])
router.include_router(onboarding_router, prefix="/onboarding", tags=["onboarding"])
router.include_router(forums_router, prefix="/forums", tags=["forums"])
router.include_router(forum_categories_router, prefix="/forums/categories", tags=["forum-categories"])
router.include_router(forum_reply_router, prefix="/forums/reply", tags=["forum-reply"])
router.include_router(pdf_router, prefix="/pdf", tags=["pdf"])