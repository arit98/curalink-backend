from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
from app.schemas.user_schema import UserCreate, UserOut, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.models.researcher_profile import ResearcherProfile 
from app.models.patient_profile import PatientProfile

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.email == user_data.email))
    existing = q.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    new_user = User(email=user_data.email, hashed_password=hash_password(user_data.password), name=user_data.name, role=user_data.role)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.email == user_data.email))
    user = q.scalar_one_or_none()
    if not user or not verify_password(user_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user_id=user.id, email=user.email, role=user.role)

    has_onboarded = False
    if user.role == 1:  # researcher
        q_profile = await db.execute(select(ResearcherProfile).where(ResearcherProfile.user_id == user.id))
        profile = q_profile.scalar_one_or_none()
        has_onboarded = bool(profile)
    elif user.role == 0:  # patient
        q_profile = await db.execute(select(PatientProfile).where(PatientProfile.user_id == user.id))
        profile = q_profile.scalar_one_or_none()
        has_onboarded = bool(profile)

    return {
        "access_token": token,
        "token_type": "Bearer",
        "id": str(user.id),
        "role": user.role,
        "has_onboarded": has_onboarded,
        "user": {
            "id": str(user.id),
            "email": user.email,
            "role": user.role
        }
    }


@router.get("/", response_model=list[UserOut])
async def list_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user