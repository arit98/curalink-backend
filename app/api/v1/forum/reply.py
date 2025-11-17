from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List
from datetime import datetime

from app.db.database import get_db
from app.models.forums_reply import ForumReply
from app.models.forums import ForumPost
from app.schemas.forums_reply import ReplyCreate, ReplyUpdate, ReplyOut

router = APIRouter(prefix="/posts", tags=["Forum Replies"])

@router.get("/{post_id}/replies", response_model=List[ReplyOut])
async def get_replies(post_id: int, db: AsyncSession = Depends(get_db)):
    # ensure post exists (optional)
    post = await db.get(ForumPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    result = await db.execute(select(ForumReply).where(ForumReply.post_id == post_id).order_by(ForumReply.timestamp.asc()))
    replies = result.scalars().all()
    return replies

@router.post("/{post_id}/replies", response_model=ReplyOut, status_code=status.HTTP_201_CREATED)
async def create_reply(post_id: int, body: ReplyCreate, db: AsyncSession = Depends(get_db)):
    post = await db.get(ForumPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    new_reply = ForumReply(
        post_id=post_id,
        author=body.author,
        role=body.role,
        content=body.content,
        timestamp=datetime.utcnow()
    )

    db.add(new_reply)

    # increment post.replies count
    post.replies = (post.replies or 0) + 1

    await db.commit()
    await db.refresh(new_reply)
    # optional: refresh post if you want to return it elsewhere
    return new_reply

@router.put("/{post_id}/replies/{reply_id}", response_model=ReplyOut)
async def edit_reply(post_id: int, reply_id: int, body: ReplyUpdate, db: AsyncSession = Depends(get_db)):
    # ensure post exists
    post = await db.get(ForumPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    reply = await db.get(ForumReply, reply_id)
    if not reply or reply.post_id != post_id:
        raise HTTPException(status_code=404, detail="Reply not found")

    if body.content is not None:
        reply.content = body.content
        reply.timestamp = datetime.utcnow()

    await db.commit()
    await db.refresh(reply)
    return reply

@router.delete("/{post_id}/replies/{reply_id}")
async def delete_reply(post_id: int, reply_id: int, db: AsyncSession = Depends(get_db)):
    post = await db.get(ForumPost, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    reply = await db.get(ForumReply, reply_id)
    if not reply or reply.post_id != post_id:
        raise HTTPException(status_code=404, detail="Reply not found")

    # delete reply and decrement post.replies
    await db.delete(reply)
    post.replies = max((post.replies or 1) - 1, 0)

    await db.commit()
    return {"message": "Reply deleted successfully"}
