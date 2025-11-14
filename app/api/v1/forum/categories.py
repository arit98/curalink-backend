from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import List

from app.db.database import get_db
from app.models.forums_category import ForumCategory

router = APIRouter()

# ---------- SCHEMAS ----------

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True


# ---------- ROUTES ----------

@router.post("/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, db: AsyncSession = Depends(get_db)):

    # Check existing
    result = await db.execute(
        select(ForumCategory).where(ForumCategory.name == category.name)
    )
    existing = result.scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists")

    new_category = ForumCategory(name=category.name)
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)

    return new_category


@router.get("/", response_model=List[CategoryResponse])
async def get_all_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ForumCategory))
    return result.scalars().all()


@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ForumCategory).where(ForumCategory.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(category_id: int, update: CategoryUpdate, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(ForumCategory).where(ForumCategory.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    category.name = update.name

    await db.commit()
    await db.refresh(category)

    return category


@router.delete("/{category_id}")
async def delete_category(category_id: int, db: AsyncSession = Depends(get_db)):

    result = await db.execute(
        select(ForumCategory).where(ForumCategory.id == category_id)
    )
    category = result.scalar_one_or_none()

    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.delete(category)
    await db.commit()

    return {"message": "Category deleted successfully"}
