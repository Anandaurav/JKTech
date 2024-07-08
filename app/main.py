from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from app.database import engine, get_db
from app import models, crud, schemas, llama3, recommender

app = FastAPI()

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.post("/books", response_model=schemas.Book)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_book(db=db, book=book)

@app.get("/books", response_model=list[schemas.Book])
async def read_books(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    return await crud.get_books(db=db, skip=skip, limit=limit)

@app.get("/books/{book_id}", response_model=schemas.Book)
async def read_book(book_id: int, db: AsyncSession = Depends(get_db)):
    db_book = await crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.put("/books/{book_id}", response_model=schemas.Book)
async def update_book(book_id: int, book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    return await crud.update_book(db=db, book_id=book_id, book=book)

@app.delete("/books/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    await crud.delete_book(db=db, book_id=book_id)
    return {"detail": "Book deleted"}

@app.post("/books/{book_id}/reviews", response_model=schemas.Review)
async def create_review(book_id: int, review: schemas.ReviewCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_review(db=db, review=review)

@app.get("/books/{book_id}/reviews", response_model=list[schemas.Review])
async def read_reviews(book_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_reviews(db=db, book_id=book_id)

@app.get("/books/{book_id}/summary")
async def get_summary(book_id: int, db: AsyncSession = Depends(get_db)):
    book = await crud.get_book(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    summary = llama3.generate_summary(book.summary)
    avg_rating = await crud.get_avg_rating(db=db, book_id=book_id)
    return {"summary": summary, "average_rating": avg_rating}

@app.get("/recommendations")
async def get_recommendations(genre: str, db: AsyncSession = Depends(get_db)):
    recommendations = await recommender.get_recommendations(genre=genre, db=db)
    return recommendations

@app.post("/generate-summary")
async def generate_summary_endpoint(content: str):
    summary = llama3.generate_summary(content)
    return {"summary": summary}
