from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.trial import Trial
from app.models.user import User
from app.models.favourite import Favourite
from app.schemas.trial_schema import TrialCreate, TrialOut
from app.core.deps import check_researcher_role

router = APIRouter()

@router.get("/", response_model=list[TrialOut])
async def list_trials(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trial))
    return result.scalars().all()


@router.post("/", response_model=TrialOut)
async def create_trial(
    trial_data: TrialCreate,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    token = authorization.split(" ")[1] if authorization else None
    check_researcher_role(token)

    # Use model-compatible dict (exclude unset to allow DB defaults)
    new_trial = Trial(**trial_data.dict(exclude_unset=True))
    db.add(new_trial)
    await db.commit()
    await db.refresh(new_trial)
    return new_trial


@router.put("/{trial_id}", response_model=TrialOut)
async def update_trial(
    trial_id: int,
    trial_data: TrialCreate,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    token = authorization.split(" ")[1] if authorization else None
    check_researcher_role(token)

    result = await db.execute(select(Trial).where(Trial.id == trial_id))
    trial = result.scalar_one_or_none()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")

    for key, value in trial_data.dict().items():
        setattr(trial, key, value)

    await db.commit()
    await db.refresh(trial)
    return trial


@router.delete("/{trial_id}")
async def delete_trial(
    trial_id: int,
    db: AsyncSession = Depends(get_db),
    authorization: str = Header(None),
):
    token = authorization.split(" ")[1] if authorization else None
    check_researcher_role(token)

    result = await db.execute(select(Trial).where(Trial.id == trial_id))
    trial = result.scalar_one_or_none()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")

    await db.delete(trial)
    await db.commit()
    return {"message": "Trial deleted successfully"}



@router.post("/{trial_id}/favourite")
async def favourite_trial(
    trial_id: int,
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

    result = await db.execute(select(Trial).where(Trial.id == trial_id))
    trial = result.scalar_one_or_none()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")

    # check existing favourite
    q = await db.execute(
        select(Favourite).where(
            Favourite.user_id == user.id,
            Favourite.content_type == "trial",
            Favourite.content_id == trial_id,
        )
    )
    existing = q.scalar_one_or_none()
    if existing:
        return {"message": "Already favourited"}

    fav = Favourite(user_id=user.id, content_type="trial", content_id=trial_id)
    db.add(fav)
    await db.commit()
    return {"message": "Added to favourites"}


@router.delete("/{trial_id}/favourite")
async def unfavourite_trial(
    trial_id: int,
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
            Favourite.content_type == "trial",
            Favourite.content_id == trial_id,
        )
    )
    fav = q.scalar_one_or_none()
    if not fav:
        raise HTTPException(status_code=404, detail="Favourite not found")

    await db.delete(fav)
    await db.commit()
    return {"message": "Removed from favourites"}


@router.get("/{trial_id}/favourite")
async def get_trial_favourite_status(
    trial_id: int,
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
            Favourite.content_type == "trial",
            Favourite.content_id == trial_id,
        )
    )
    fav = q.scalar_one_or_none()
    return {"favourited": bool(fav)}