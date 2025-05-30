from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app import models, schemas, database
from typing import List

router = APIRouter()

@router.post("/", response_model=schemas.BookOut)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(database.get_db)):
    db_book = models.Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[schemas.BookOut])
async def get_books(db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Book))
    return result.scalars().all()

@router.get("/{book_id}", response_model=schemas.BookOut)
async def get_book(book_id: int, db: AsyncSession = Depends(database.get_db)):
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    book = result.scalars().first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book
