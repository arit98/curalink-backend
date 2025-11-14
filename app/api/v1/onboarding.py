from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
from app.models.researcher_profile import ResearcherProfile
from app.models.patient_profile import PatientProfile
from app.schemas.onboarding_schema import ResearcherProfileCreate, PatientProfileCreate
from app.core.security import decode_access_token
from fastapi.security import HTTPBearer

router = APIRouter()
security = HTTPBearer()

# --- Helper ---
async def get_current_user(token: str = Depends(security), db: AsyncSession = Depends(get_db)) -> User:
    payload = decode_access_token(token.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user_id = payload.get("userId")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")

    q = await db.execute(select(User).where(User.id == user_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


# --- Researcher onboarding ---
@router.post("/researcher", status_code=status.HTTP_201_CREATED)
async def create_researcher_profile(
    profile_data: ResearcherProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 1:
        raise HTTPException(status_code=403, detail="Only researchers can access this route")

    profile = ResearcherProfile(
        user_id=current_user.id,
        condition=profile_data.condition,
        location=profile_data.location,
        tags=",".join(profile_data.tags or [])
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return {"message": "Researcher onboarding completed", "profile": profile}


# --- Patient onboarding ---
@router.post("/patient", status_code=status.HTTP_201_CREATED)
async def create_patient_profile(
    profile_data: PatientProfileCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 0:
        raise HTTPException(status_code=403, detail="Only patients can access this route")

    profile = PatientProfile(
        user_id=current_user.id,
        condition=profile_data.condition,
        location=profile_data.location
    )
    db.add(profile)
    await db.commit()
    await db.refresh(profile)
    return {"message": "Patient onboarding completed", "profile": profile}

    

@router.get("/status")
async def get_onboarding_status(current_user: User = Depends(get_current_user)):
    return {"has_onboarded": current_user.has_onboarded, "role": current_user.role}
