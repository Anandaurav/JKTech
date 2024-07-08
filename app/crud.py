from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import Book, Review
from app.schemas import BookCreate, ReviewCreate

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(Book).offset(skip).limit(limit))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int):
    result = await db.execute(select(Book).filter(Book.id == book_id))
    return result.scalar_one_or_none()

async def create_book(db: AsyncSession, book: BookCreate):
    db_book = Book(**book.dict())
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def update_book(db: AsyncSession, book_id: int, book: BookCreate):
    db_book = await get_book(db, book_id)
    for key, value in book.dict().items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, book_id: int):
    db_book = await get_book(db, book_id)
    await db.delete(db_book)
    await db.commit()

async def create_review(db: AsyncSession, review: ReviewCreate):
    db_review = Review(**review.dict())
    db.add(db_review)
    await db.commit()
    await db.refresh(db_review)
    return db_review

async def get_reviews(db: AsyncSession, book_id: int):
    result = await db.execute(select(Review).filter(Review.book_id == book_id))
    return result.scalars().all()

async def get_avg_rating(db: AsyncSession, book_id: int):
    result = await db.execute(select(func.avg(Review.rating)).filter(Review.book_id == book_id))
    return result.scalar()
