from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app import schemas, models, auth
from typing import List
import httpx

router = APIRouter()

BOOK_SERVICE_URL = "http://127.0.0.1:8001/books/"

@router.post("/", response_model=schemas.ReviewOut)
async def add_review(
    review: schemas.ReviewCreate,
    db: AsyncSession = Depends(get_db),
    user_email: str = Depends(auth.get_current_user)
):
    # Verify book exists
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{BOOK_SERVICE_URL}{review.book_id}")
        if res.status_code != 200:
            raise HTTPException(status_code=404, detail="Book not found")

    new_review = models.Review(**review.dict(), user_email=user_email)
    db.add(new_review)
    await db.commit()
    await db.refresh(new_review)
    return new_review

@router.get("/book/{book_id}", response_model=List[schemas.ReviewOut])
async def get_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Review).where(models.Review.book_id == book_id))
    return result.scalars().all()
