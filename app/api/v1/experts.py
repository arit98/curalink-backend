from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.expert import Expert
from app.models.user import User
from app.models.favourite import Favourite
from app.schemas.expert_schema import ExpertCreate, ExpertOut
from app.core.deps import check_researcher_role

router = APIRouter()


@router.get("/", response_model=list[ExpertOut])
async def list_experts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Expert))
    return result.scalars().all()


@router.post("/", response_model=ExpertOut)
async def create_expert(
    expert_data: ExpertCreate,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    token = authorization.split(" ")[1] if authorization else None
    check_researcher_role(token)

    new_expert = Expert(**expert_data.dict(exclude_unset=True))
    db.add(new_expert)
    await db.commit()
    await db.refresh(new_expert)
    return new_expert


@router.post("/{expert_id}/favourite")
async def favourite_expert(
    expert_id: int,
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

    result = await db.execute(select(Expert).where(Expert.id == expert_id))
    expert = result.scalar_one_or_none()
    if not expert:
        raise HTTPException(status_code=404, detail="Expert not found")

    q = await db.execute(
        select(Favourite).where(
            Favourite.user_id == user.id,
            Favourite.content_type == "expert",
            Favourite.content_id == expert_id,
        )
    )
    existing = q.scalar_one_or_none()
    if existing:
        return {"message": "Already favourited"}

    fav = Favourite(user_id=user.id, content_type="expert", content_id=expert_id)
    db.add(fav)
    await db.commit()
    return {"message": "Added to favourites"}


@router.delete("/{expert_id}/favourite")
async def unfavourite_expert(
    expert_id: int,
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

    q = await db.execute(
        select(Favourite).where(
            Favourite.user_id == user.id,
            Favourite.content_type == "expert",
            Favourite.content_id == expert_id,
        )
    )
    fav = q.scalar_one_or_none()
    if not fav:
        raise HTTPException(status_code=404, detail="Favourite not found")

    await db.delete(fav)
    await db.commit()
    return {"message": "Removed from favourites"}


@router.get("/{expert_id}/favourite")
async def get_expert_favourite_status(
    expert_id: int,
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

    q = await db.execute(
        select(Favourite).where(
            Favourite.user_id == user.id,
            Favourite.content_type == "expert",
            Favourite.content_id == expert_id,
        )
    )
    fav = q.scalar_one_or_none()
    return {"favourited": bool(fav)}


