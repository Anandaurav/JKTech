import pickle
from sqlalchemy.future import select
from app.models import Book

# Load the pretrained model
with open('recommendation_model.pkl', 'rb') as f:
    model = pickle.load(f)

async def get_recommendations(genre: str, db):
    genre_code = genre
    result = await db.execute(select(Book).filter(Book.genre == genre_code))
    books = result.scalars().all()
    features = [[book.genre, book.average_rating] for book in books]
    recommendations = model.predict(features)
    return recommendations
