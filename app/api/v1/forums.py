from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.models.forums import ForumPost
from app.models.forums_category import ForumCategory
from app.schemas.forums import ForumPostCreate, ForumPostUpdate, ForumPostOut

router = APIRouter()

@router.post("/posts", response_model=ForumPostOut)
async def create_post(post: ForumPostCreate, db: AsyncSession = Depends(get_db)):
    new_post = ForumPost(**post.dict(), timestamp=datetime.utcnow())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)
    return new_post

@router.get("/posts", response_model=List[ForumPostOut])
async def get_posts(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ForumPost))
    posts = result.scalars().all()
    return posts

@router.get("/posts/{post_id}", response_model=ForumPostOut)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(ForumPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/posts/{post_id}", response_model=ForumPostOut)
async def update_post(post_id: int, updated: ForumPostUpdate, db: AsyncSession = Depends(get_db)):
    post = await db.get(ForumPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    for key, value in updated.dict(exclude_unset=True).items():
        setattr(post, key, value)
    await db.commit()
    await db.refresh(post)
    return post

@router.delete("/posts/{post_id}")
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(ForumPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    await db.delete(post)
    await db.commit()
    return {"message": f"Post {post_id} deleted successfully."}

@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ForumCategory))
    categories = result.scalars().all()
    return categories
