from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
from app.models.favourite import Favourite
from app.core.deps import check_researcher_role

router = APIRouter()

@router.get("/")
async def list_user_favourites(
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    token = authorization.split(" ")[1] if authorization else None
    payload = check_researcher_role(token)

    # resolve researcher user by preferring `email`, then `userId`, then `sub`.
    sub = payload.get("email") or payload.get("userId") or payload.get("sub")
    user = None
    if sub is not None:
        if isinstance(sub, str) and "@" in sub:
            q = await db.execute(select(User).where(User.email == sub))
            user = q.scalar_one_or_none()
        else:
            try:
                user_id = int(sub)
                q = await db.execute(select(User).where(User.id == user_id))
                user = q.scalar_one_or_none()
            except (ValueError, TypeError):
                q = await db.execute(select(User).where(User.email == str(sub)))
                user = q.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=401, detail="Researcher not found")

    q = await db.execute(select(Favourite).where(Favourite.user_id == user.id))
    favs = q.scalars().all()

    # return simple serializable objects
    return [
        {
            "id": f.id,
            "content_type": f.content_type,
            "content_id": f.content_id,
            "created_at": f.created_at.isoformat() if f.created_at else None,
        }
        for f in favs
    ]


