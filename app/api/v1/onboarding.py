from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.database import get_db
from app.models.user import User
from app.models.researcher_profile import ResearcherProfile
from app.models.patient_profile import PatientProfile
from app.schemas.onboarding_schema import (
    ResearcherProfileCreate, 
    ResearcherProfileUpdate,
    PatientProfileCreate,
    PatientProfileUpdate
)
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


@router.get("/researcher")
async def get_researcher_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 1:
        raise HTTPException(status_code=403, detail="Only researchers can access this route")
    
    q = await db.execute(select(ResearcherProfile).where(ResearcherProfile.user_id == current_user.id))
    profile = q.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Researcher profile not found")
    
    return {
        "id": profile.id,
        "condition": profile.condition,
        "location": profile.location,
        "tags": profile.tags.split(",") if profile.tags else []
    }


@router.get("/researcher/{profile_id}")
async def get_researcher_profile_by_id(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = await db.execute(select(ResearcherProfile).where(ResearcherProfile.id == profile_id))
    profile = q.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Researcher profile not found")
    
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "condition": profile.condition,
        "location": profile.location,
        "tags": profile.tags.split(",") if profile.tags else []
    }


@router.put("/researcher")
async def update_researcher_profile(
    profile_data: ResearcherProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 1:
        raise HTTPException(status_code=403, detail="Only researchers can access this route")
    
    q = await db.execute(
        select(ResearcherProfile).where(ResearcherProfile.user_id == current_user.id)
    )
    profile = q.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Researcher profile not found")
    
    # Update only provided fields
    if profile_data.condition is not None:
        profile.condition = profile_data.condition
    if profile_data.location is not None:
        profile.location = profile_data.location
    if profile_data.tags is not None:
        profile.tags = ",".join(profile_data.tags) if profile_data.tags else None
    
    await db.commit()
    await db.refresh(profile)
    return {"message": "Researcher profile updated", "profile": profile}


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


@router.get("/patient")
async def get_patient_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 0:
        raise HTTPException(status_code=403, detail="Only patients can access this route")
    
    q = await db.execute(select(PatientProfile).where(PatientProfile.user_id == current_user.id))
    profile = q.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    
    return {
        "id": profile.id,
        "condition": profile.condition,
        "location": profile.location
    }


@router.get("/patient/{profile_id}")
async def get_patient_profile_by_id(
    profile_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    q = await db.execute(select(PatientProfile).where(PatientProfile.id == profile_id))
    profile = q.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    
    return {
        "id": profile.id,
        "user_id": profile.user_id,
        "condition": profile.condition,
        "location": profile.location
    }


@router.put("/patient")
async def update_patient_profile(
    profile_data: PatientProfileUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != 0:
        raise HTTPException(status_code=403, detail="Only patients can access this route")
    
    q = await db.execute(
        select(PatientProfile).where(PatientProfile.user_id == current_user.id)
    )
    profile = q.scalar_one_or_none()
    if not profile:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient profile not found")
    
    # Update only provided fields
    if profile_data.condition is not None:
        profile.condition = profile_data.condition
    if profile_data.location is not None:
        profile.location = profile_data.location
    
    await db.commit()
    await db.refresh(profile)
    return {"message": "Patient profile updated", "profile": profile}


@router.get("/status")
async def get_onboarding_status(current_user: User = Depends(get_current_user)):
    return {"has_onboarded": current_user.has_onboarded, "role": current_user.role}
