from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.publication import Publication
from app.models.user import User
from app.models.favourite import Favourite
from app.schemas.publication_schema import PublicationCreate, PublicationOut
from app.core.deps import check_researcher_role

router = APIRouter()


@router.get("/", response_model=list[PublicationOut])
async def list_publications(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Publication))
    return result.scalars().all()


@router.post("/", response_model=PublicationOut)
async def create_publication(
    publication_data: PublicationCreate,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    token = authorization.split(" ")[1] if authorization else None
    check_researcher_role(token)

    new_pub = Publication(**publication_data.dict(exclude_unset=True))
    db.add(new_pub)
    await db.commit()
    await db.refresh(new_pub)
    return new_pub


@router.post("/{publication_id}/favourite")
async def favourite_publication(
    publication_id: int,
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

    result = await db.execute(select(Publication).where(Publication.id == publication_id))
    pub = result.scalar_one_or_none()
    if not pub:
        raise HTTPException(status_code=404, detail="Publication not found")

    q = await db.execute(
        select(Favourite).where(
            Favourite.user_id == user.id,
            Favourite.content_type == "publication",
            Favourite.content_id == publication_id,
        )
    )
    existing = q.scalar_one_or_none()
    if existing:
        return {"message": "Already favourited"}

    fav = Favourite(user_id=user.id, content_type="publication", content_id=publication_id)
    db.add(fav)
    await db.commit()
    return {"message": "Added to favourites"}


@router.delete("/{publication_id}/favourite")
async def unfavourite_publication(
    publication_id: int,
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
            Favourite.content_type == "publication",
            Favourite.content_id == publication_id,
        )
    )
    fav = q.scalar_one_or_none()
    if not fav:
        raise HTTPException(status_code=404, detail="Favourite not found")

    await db.delete(fav)
    await db.commit()
    return {"message": "Removed from favourites"}


@router.get("/{publication_id}/favourite")
async def get_publication_favourite_status(
    publication_id: int,
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
            Favourite.content_type == "publication",
            Favourite.content_id == publication_id,
        )
    )
    fav = q.scalar_one_or_none()
    return {"favourited": bool(fav)}


